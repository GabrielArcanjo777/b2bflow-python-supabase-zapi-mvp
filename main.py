import os
from typing import Any

import requests
from dotenv import load_dotenv


MESSAGE_TEMPLATE = "Olá, {nome} tudo bem com você?"
CONTACT_LIMIT = 3


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Variável de ambiente obrigatória ausente: {name}")
    return value


def fetch_contacts(
    supabase_url: str,
    supabase_key: str,
    table_name: str,
    limit: int = CONTACT_LIMIT,
) -> list[dict[str, Any]]:
    base_url = supabase_url.rstrip("/")
    url = f"{base_url}/rest/v1/{table_name}"
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
    }
    params = {
        "select": "nome,telefone",
        "limit": str(limit),
    }

    response = requests.get(url, headers=headers, params=params, timeout=15)
    response.raise_for_status()
    return response.json()


def build_message(contact_name: str) -> str:
    return MESSAGE_TEMPLATE.format(nome=contact_name.strip())


def main() -> None:
    load_dotenv()

    supabase_url = get_required_env("SUPABASE_URL")
    supabase_key = get_required_env("SUPABASE_KEY")
    table_name = os.getenv("SUPABASE_TABLE", "contacts")

    contacts = fetch_contacts(supabase_url, supabase_key, table_name)
    if not contacts:
        print("Nenhum contato encontrado.")
        return

    for contact in contacts:
        name = str(contact.get("nome", "")).strip()
        phone = str(contact.get("telefone", "")).strip()
        if not name or not phone:
            print("Contato ignorado por falta de nome ou telefone.")
            continue

        message = build_message(name)
        print(f"Mensagem preparada para {name}: {message}")


if __name__ == "__main__":
    main()
