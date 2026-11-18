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
├── tests/
├── .github/workflows/ci.yml
├── .env.example
├── .gitignore
└── README.md
```

## Configurar a tabela no Supabase

No Supabase, acesse **SQL Editor** e execute o conteúdo do arquivo `setup.sql`.

O script habilita **Row Level Security (RLS)** e remove o acesso dos papéis públicos `anon` e `authenticated`. Se a tabela já existia, execute novamente a versão atual do `setup.sql` para aplicar esse endurecimento.

A tabela esperada é `public.contacts`, com os campos:

| Campo | Descrição |
|---|---|
| `id` | Identificador gerado pelo banco |
| `nome` | Nome usado para personalizar a mensagem |
| `telefone` | Telefone em formato internacional, somente dígitos |
| `created_at` | Data de criação do registro |

O `setup.sql` também cria `public.deliveries`:

| Campo | Descrição |
|---|---|
| `phone` | Telefone já atendido (chave primária) |
| `status` | `sent` ou `failed` |
| `attempts` | Quantas execuções passaram por ali |
| `sent_at` | Momento do registro |

É essa tabela que impede o mesmo contato de receber a mensagem duas vezes. **Se ela não existir, o worker para com erro** em vez de enviar duplicado — de propósito.

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
SUPABASE_KEY=sua_chave_secreta_de_backend
SUPABASE_TABLE=contacts

CONTACT_LIMIT=3
DRY_RUN=true
LIVE_SEND_CONFIRM=

ZAPI_INSTANCE_ID=sua_instancia
ZAPI_TOKEN=seu_token_zapi
ZAPI_CLIENT_TOKEN=seu_client_token_zapi

REQUEST_TIMEOUT=15
SEND_DELAY_SECONDS=1
DELIVERY_TABLE=deliveries
MAX_ATTEMPTS=3
RETRY_BACKOFF_SECONDS=0.5
```

O arquivo `.env` deve ficar apenas na máquina local e não deve ser commitado. `SUPABASE_KEY` precisa ser uma chave **secret/backend** usada somente por este worker; nunca use uma chave `publishable` ou `anon` para acessar os contatos.

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

Nesse modo seguro, o projeto busca até três contatos, monta a mensagem personalizada e mostra no terminal o que seria enviado. Nenhuma mensagem real é disparada. Valores inválidos em `DRY_RUN`, como erros de digitação, interrompem a execução.

Para enviar mensagens reais, use apenas contatos próprios ou autorizados, altere no `.env`:

```env
DRY_RUN=false
LIVE_SEND_CONFIRM=I_UNDERSTAND
```

Depois execute novamente:

```bash
python main.py
```

O worker consulta `public.deliveries` antes de enviar. Contato já registrado como `sent` é ignorado, então rodar o script mais de uma vez **não duplica** a mensagem.

Se o `setup.sql` não tiver sido aplicado, o worker para com erro pedindo a tabela — prefere falhar a mandar duas vezes.

### Retry

Falhas transitórias (`408`, `425`, `429`, `5xx`, timeout de rede) são repetidas com backoff exponencial, até `MAX_ATTEMPTS`. Erro `4xx` **não** é repetido: a requisição está errada e insistir só aumenta o risco de bloqueio do número.

## Executar os testes

```bash
python -m unittest discover -s tests -v
```

O GitHub Actions executa os testes nas versões suportadas do Python e audita as dependências em cada pull request.

## Cuidados com credenciais

- `.env` está no `.gitignore`.
- O repositório deve conter apenas `.env.example`.
- Credenciais devem ficar somente em variáveis de ambiente.
- Chaves `publishable`/`anon` do Supabase não devem acessar a tabela de contatos.
- RLS e revogação dos papéis públicos fazem parte do `setup.sql`.
- Não use dados reais em `setup.sql` ou na documentação.
- O código mascara telefones nos logs.
- Telefones duplicados são ignorados antes do envio.

## Como foi feito

O projeto foi escrito com apoio de IA generativa. A divis�o real do trabalho, o que est� verificado e o que n�o est�: [docs/como-foi-feito.md](docs/como-foi-feito.md).
