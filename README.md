# b2bflow Python + Supabase + Z-API

MVP técnico em Python para ler contatos autorizados no Supabase e enviar uma mensagem personalizada via Z-API.

A mensagem enviada é:

```txt
Olá, <nome_contato> tudo bem com você?
```

O projeto foi mantido propositalmente simples para facilitar revisão em entrevista: execução local, variáveis de ambiente, modo seguro de simulação e limite máximo de três contatos por execução.

## Tecnologias

- Python
- Supabase REST API
- Z-API
- python-dotenv
- requests

## Estrutura

```txt
.
├── main.py
├── requirements.txt
├── setup.sql
├── .env.example
├── .gitignore
├── README.md
├── COMMITS.md
└── PROMPTS_CODEX.md
```

## Configurar a tabela no Supabase

No Supabase, acesse **SQL Editor** e execute o arquivo `setup.sql`.

A tabela esperada é `public.contacts`, com os campos:

| Campo | Descrição |
|---|---|
| `id` | Identificador gerado pelo banco |
| `nome` | Nome usado para personalizar a mensagem |
| `telefone` | Telefone em formato internacional, somente dígitos |
| `created_at` | Data de criação do registro |

Use apenas contatos fictícios, próprios ou explicitamente autorizados. Não coloque números reais no repositório.

## Configurar variáveis de ambiente

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

No Windows, se preferir:

```powershell
copy .env.example .env
```

Preencha o `.env` local com seus dados:

```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_chave_supabase
SUPABASE_TABLE=contacts

CONTACT_LIMIT=3
DRY_RUN=true

ZAPI_INSTANCE_ID=sua_instancia
ZAPI_TOKEN=seu_token_zapi
ZAPI_CLIENT_TOKEN=seu_client_token_zapi

REQUEST_TIMEOUT=15
SEND_DELAY_SECONDS=1
```

O arquivo `.env` não deve ser commitado. O repositório deve conter apenas `.env.example`.

## Instalar dependências

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Rodar em modo simulação

Mantenha `DRY_RUN=true` no `.env` e execute:

```bash
python main.py
```

Nesse modo o projeto busca até três contatos, monta a mensagem e mostra no terminal o que seria enviado. Nenhuma mensagem real é disparada.

## Enviar mensagens reais

Depois de validar com contatos próprios ou autorizados, altere no `.env`:

```env
DRY_RUN=false
```

Execute novamente:

```bash
python main.py
```

Os telefones exibidos no terminal são mascarados para evitar exposição completa nos logs.

## Segurança

- `.env` está no `.gitignore`.
- Credenciais ficam apenas em variáveis de ambiente.
- `DRY_RUN=true` é o padrão recomendado para testes.
- O envio é limitado a no máximo três contatos por execução.
- O código não registra telefone completo nos logs.
- `setup.sql` não inclui dados reais.

## Histórico de commits

O arquivo `COMMITS.md` contém uma sequência sugerida de commits pequenos e objetivos para explicar a evolução do MVP.
