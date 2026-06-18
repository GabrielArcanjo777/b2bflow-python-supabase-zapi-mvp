# b2bflow Python + Supabase + Z-API

MVP técnico em Python para ler contatos autorizados no Supabase e enviar uma mensagem personalizada via Z-API.

A mensagem enviada é:

```txt
Olá, <nome_contato> tudo bem com você?
```

O projeto roda localmente, usa variáveis de ambiente para credenciais e vem com `DRY_RUN=true` para testar sem enviar mensagens reais.

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
└── README.md
```

## Configurar a tabela no Supabase

No Supabase, acesse **SQL Editor** e execute o conteúdo do arquivo `setup.sql`.

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

Preencha o `.env` local:

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

O arquivo `.env` deve ficar apenas na máquina local e não deve ser commitado.

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

## Executar o projeto

Com `DRY_RUN=true` no `.env`, rode:

```bash
python main.py
```

Nesse modo seguro, o projeto busca até três contatos, monta a mensagem personalizada e mostra no terminal o que seria enviado. Nenhuma mensagem real é disparada.

Para enviar mensagens reais, use apenas contatos próprios ou autorizados, altere no `.env`:

```env
DRY_RUN=false
```

Depois execute novamente:

```bash
python main.py
```

## Cuidados com credenciais

- `.env` está no `.gitignore`.
- O repositório deve conter apenas `.env.example`.
- Credenciais devem ficar somente em variáveis de ambiente.
- Não use dados reais em `setup.sql` ou na documentação.
- O código mascara telefones nos logs.
- Telefones duplicados são ignorados antes do envio.
