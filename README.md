# B2BFlow — Supabase + Z-API

Worker em Python para consultar contatos autorizados no Supabase e enviar mensagens personalizadas pela Z-API. O modo seguro (`DRY_RUN=true`) vem ativado por padrão, permitindo validar configuração e conteúdo sem realizar envios.

## Objetivo

Demonstrar uma integração de backend pequena, testável e orientada a segurança:

- credenciais carregadas por variáveis de ambiente;
- limite máximo de três contatos por execução;
- rejeição de chaves públicas do Supabase;
- confirmação explícita antes de qualquer envio real;
- telefones mascarados nos logs;
- contatos inválidos ou duplicados ignorados;
- timeouts e erros externos tratados.

## Fluxo

```text
Configuração
    ↓
Supabase REST API
    ↓
Validação e deduplicação
    ↓
Composição da mensagem
    ↓
DRY_RUN ── sim ──> prévia segura no terminal
    │
    não
    ↓
confirmação explícita + Z-API
```

## Decisões de código

O contato é imutável, evitando alterações acidentais durante o processamento:

```python
@dataclass(frozen=True)
class Contact:
    nome: str
    telefone: str
```

O telefone é normalizado em um único ponto. A mesma regra é reutilizada na validação, na deduplicação e no mascaramento dos logs:

```python
def normalize_phone(phone: str) -> str:
    return "".join(char for char in phone if char.isdigit())
```

O envio real exige duas decisões independentes: desativar o modo de simulação e fornecer a frase de confirmação. Isso reduz o risco de uma configuração incompleta disparar mensagens:

```env
DRY_RUN=false
LIVE_SEND_CONFIRM=I_UNDERSTAND
```

Os comentários no código ficam reservados para decisões e restrições que não são óbvias. Nomes claros, funções pequenas e testes explicam o restante.

## Estrutura atual

```text
.
├── main.py                 # configuração, integração e orquestração
├── tests/test_main.py      # testes unitários e de segurança
├── setup.sql               # tabela e políticas do Supabase
├── .env.example            # configuração sem segredos
├── requirements.txt
└── .github/workflows/ci.yml
```

Para o tamanho atual do projeto, um módulo principal mantém a execução simples. Quando novas integrações ou regras forem adicionadas, a evolução recomendada é separar `config`, `domain`, `supabase_client`, `zapi_client` e `service`, preservando a mesma interface pública coberta pelos testes.

## Configuração

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Linux ou macOS:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Crie a tabela executando `setup.sql` no SQL Editor do Supabase. Depois, preencha o `.env` local. Nunca versione o arquivo `.env`.

## Execução segura

Mantenha no `.env`:

```env
DRY_RUN=true
CONTACT_LIMIT=3
```

Execute:

```bash
python main.py
```

O terminal mostrará apenas uma prévia, com os números mascarados. Nenhuma mensagem será enviada.

## Testes

```bash
python -m unittest discover -s tests -v
```

O mesmo conjunto deve ser executado pelo GitHub Actions antes de uma alteração chegar à branch principal.

## Uso responsável

Use somente contatos próprios, fictícios ou explicitamente autorizados. O projeto não implementa gestão de consentimento, opt-out, campanhas ou conformidade completa para uso comercial em produção.
