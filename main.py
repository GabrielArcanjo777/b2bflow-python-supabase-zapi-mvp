import base64
import json
import logging
import os
import time
from dataclasses import dataclass

import requests
from dotenv import load_dotenv


MESSAGE_TEMPLATE = "Olá, {nome} tudo bem com você?"
CONTACT_LIMIT_MAX = 3
DEFAULT_REQUEST_TIMEOUT = 15.0
DEFAULT_SEND_DELAY_SECONDS = 1.0
TRUE_VALUES = {"1", "true", "yes", "y", "sim", "s"}
FALSE_VALUES = {"0", "false", "no", "n", "nao", "não"}
LIVE_SEND_CONFIRMATION = "I_UNDERSTAND"


@dataclass(frozen=True)
class Contact:
    nome: str
    telefone: str


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Variável de ambiente obrigatória ausente: {name}")
    return value


def get_bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default

    normalized = value.strip().lower()
    if normalized in TRUE_VALUES:
        return True
    if normalized in FALSE_VALUES:
        return False
    raise RuntimeError(
        f"Variável {name} deve usar um valor booleano explícito "
        "(true/false, 1/0, yes/no ou sim/não)."
    )


def get_jwt_role(token: str) -> str | None:
    """Lê somente o papel declarado no payload JWT, sem validar o token."""
    parts = token.split(".")
    if len(parts) != 3:
        return None

    try:
        payload = parts[1] + "=" * (-len(parts[1]) % 4)
        decoded = base64.urlsafe_b64decode(payload.encode("ascii"))
        data = json.loads(decoded)
    except (UnicodeError, ValueError, json.JSONDecodeError):
        return None

    role = data.get("role")
    return role if isinstance(role, str) else None


def validate_supabase_backend_key(key: str) -> str:
    """Rejeita chaves reconhecidamente destinadas a clientes públicos."""
    if key.startswith("sb_publishable_") or get_jwt_role(key) == "anon":
        raise RuntimeError(
            "SUPABASE_KEY não pode ser uma chave publishable/anon. "
            "Use uma chave secreta apenas neste worker de backend."
        )
    return key


def require_live_send_confirmation() -> None:
    confirmation = os.getenv("LIVE_SEND_CONFIRM", "")
    if confirmation != LIVE_SEND_CONFIRMATION:
        raise RuntimeError(
            "Envio real bloqueado. Defina "
            f"LIVE_SEND_CONFIRM={LIVE_SEND_CONFIRMATION} para confirmar."
        )


def get_int_env(name: str, default: int, minimum: int = 1) -> int:
    value = os.getenv(name)
    if value is None:
        return default

    try:
        parsed = int(value)
    except ValueError as exc:
        raise RuntimeError(f"Variável {name} deve ser um número inteiro.") from exc

    if parsed < minimum:
        raise RuntimeError(f"Variável {name} deve ser maior ou igual a {minimum}.")
    return parsed


def get_float_env(name: str, default: float, minimum: float = 0.0) -> float:
    value = os.getenv(name)
    if value is None:
        return default

    try:
        parsed = float(value)
    except ValueError as exc:
        raise RuntimeError(f"Variável {name} deve ser numérica.") from exc

    if parsed < minimum:
        raise RuntimeError(f"Variável {name} deve ser maior ou igual a {minimum}.")
    return parsed


def normalize_phone(phone: str) -> str:
    return "".join(char for char in phone if char.isdigit())


def mask_phone(phone: str) -> str:
    digits = normalize_phone(phone)
    if len(digits) <= 4:
        return "*" * len(digits)
    return f"{'*' * (len(digits) - 4)}{digits[-4:]}"


def fetch_contacts(
    supabase_url: str,
    supabase_key: str,
    table_name: str,
    limit: int,
    timeout: float,
) -> list[Contact]:
    base_url = supabase_url.rstrip("/")
    url = f"{base_url}/rest/v1/{table_name}"
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
    }
    params: dict[str, str | int] = {
        "select": "nome,telefone",
        "limit": limit,
        "order": "created_at.asc",
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=timeout)
    except requests.RequestException as exc:
        raise RuntimeError("Falha ao buscar contatos no Supabase.") from exc

    if not response.ok:
        raise RuntimeError(f"Supabase retornou HTTP {response.status_code}.")

    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError("Supabase retornou uma resposta inválida.") from exc

    if not isinstance(data, list):
        raise RuntimeError("Resposta inesperada do Supabase.")

    contacts: list[Contact] = []
    used_phones: set[str] = set()

    for row in data:
        if not isinstance(row, dict):
            logging.warning("Contato ignorado por formato inválido.")
            continue

        nome = str(row.get("nome", "")).strip()
        telefone = normalize_phone(str(row.get("telefone", "")))

        if not nome or not telefone:
            logging.warning("Contato ignorado por nome/telefone ausente ou inválido.")
            continue

        if telefone in used_phones:
            logging.warning(
                "Contato ignorado por telefone duplicado: %s",
                mask_phone(telefone),
            )
            continue

        used_phones.add(telefone)
        contacts.append(Contact(nome=nome, telefone=telefone))

        if len(contacts) >= limit:
            break

    return contacts


def build_message(contact_name: str) -> str:
    return MESSAGE_TEMPLATE.format(nome=contact_name.strip())


def send_text_message(
    instance_id: str,
    token: str,
    client_token: str,
    phone: str,
    message: str,
    timeout: float,
) -> None:
    url = f"https://api.z-api.io/instances/{instance_id}/token/{token}/send-text"
    headers = {
        "Client-Token": client_token,
        "Content-Type": "application/json",
    }
    payload = {
        "phone": phone,
        "message": message,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=timeout)
    except requests.RequestException as exc:
        raise RuntimeError("Falha ao enviar mensagem pela Z-API.") from exc

    if not response.ok:
        raise RuntimeError(f"Z-API retornou HTTP {response.status_code}.")


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    load_dotenv()

    supabase_url = get_required_env("SUPABASE_URL")
    supabase_key = validate_supabase_backend_key(get_required_env("SUPABASE_KEY"))
    table_name = os.getenv("SUPABASE_TABLE", "contacts")
    dry_run = get_bool_env("DRY_RUN", default=True)
    contact_limit = min(
        get_int_env("CONTACT_LIMIT", default=CONTACT_LIMIT_MAX),
        CONTACT_LIMIT_MAX,
    )
    request_timeout = get_float_env(
        "REQUEST_TIMEOUT",
        default=DEFAULT_REQUEST_TIMEOUT,
        minimum=1.0,
    )
    send_delay = get_float_env(
        "SEND_DELAY_SECONDS",
        default=DEFAULT_SEND_DELAY_SECONDS,
        minimum=0.0,
    )

    if dry_run:
        print("DRY_RUN ativo: nenhuma mensagem real será enviada.")
    else:
        require_live_send_confirmation()
        zapi_instance_id = get_required_env("ZAPI_INSTANCE_ID")
        zapi_token = get_required_env("ZAPI_TOKEN")
        zapi_client_token = get_required_env("ZAPI_CLIENT_TOKEN")

    contacts = fetch_contacts(
        supabase_url=supabase_url,
        supabase_key=supabase_key,
        table_name=table_name,
        limit=contact_limit,
        timeout=request_timeout,
    )
    if not contacts:
        print("Nenhum contato encontrado.")
        return

    for contact in contacts:
        name = contact.nome
        phone = contact.telefone

        message = build_message(name)
        safe_phone = mask_phone(phone)

        if dry_run:
            print(f"[DRY_RUN] {name} ({safe_phone}): {message}")
            continue

        send_text_message(
            instance_id=zapi_instance_id,
            token=zapi_token,
            client_token=zapi_client_token,
            phone=phone,
            message=message,
            timeout=request_timeout,
        )
        print(f"Mensagem enviada para {name} ({safe_phone}).")
        time.sleep(send_delay)


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(f"Erro: {error}")
        raise SystemExit(1) from error
