# b2bflow — Python + Supabase + Z-API

[![CI](https://github.com/GabrielArcanjo777/b2bflow-python-supabase-zapi-mvp/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/GabrielArcanjo777/b2bflow-python-supabase-zapi-mvp/actions/workflows/ci.yml)

Worker em Python que lê até três contatos autorizados numa tabela do Supabase e manda para cada um, via Z-API (WhatsApp), a mensagem:

```txt
Olá, <nome_contato> tudo bem com você?
```

Projeto de estudo. O envio é a parte simples; o que interessa aqui são as travas para **não** mandar mensagem errada, duplicada ou para quem não autorizou.

## O problema

Um script que dispara mensagem real tem três jeitos fáceis de dar errado:

1. rodar sem querer em modo real;
2. rodar duas vezes e mandar duas vezes;
3. vazar a chave do banco ou o telefone de alguém.

Cada trava abaixo responde a um desses.

## Como funciona

```text
.env ──► valida configuração ──► DRY_RUN? ── sim ──► só imprime o que seria enviado
                                     │
                                    não (exige LIVE_SEND_CONFIRM=I_UNDERSTAND)
                                     │
Supabase: contacts ──► até 3 contatos, sem telefone repetido
                                     │
         para cada contato: já está em deliveries como 'sent'? ── sim ──► pula
                                     │ não
                        Z-API send-text (retry só no que é seguro repetir)
                                     │
                         grava em deliveries (phone = chave primária)
```

Todo o código está em [`main.py`](main.py); os testes em [`tests/test_main.py`](tests/test_main.py).

## Travas de segurança

| Trava | Onde |
|---|---|
| `DRY_RUN=true` é o padrão; valor inválido para a execução | `get_bool_env` |
| Envio real exige `DRY_RUN=false` **e** `LIVE_SEND_CONFIRM=I_UNDERSTAND` | `require_live_send_confirmation` |
| Chave `anon`/`publishable` do Supabase é recusada | `validate_supabase_backend_key` |
| RLS ligado e acesso de `anon`/`authenticated` revogado nas duas tabelas | `setup.sql` |
| Tabela `deliveries` impede reenvio; se ela não existir, o worker para | `was_delivered`, `mark_delivered` |
| Retry só em `408/425/429/5xx` e em timeout de **conexão** | `send_text_message` |
| Timeout de **leitura** para o worker: a mensagem pode ter saído | `send_text_message` |
| Telefone mascarado no log (`*********0000`) | `mask_phone` |

## Como rodar

1. No **SQL Editor** do Supabase, execute [`setup.sql`](setup.sql). Ele cria `contacts` e `deliveries` com RLS.
2. Cadastre só contatos fictícios, seus ou que autorizaram.
3. Configure o ambiente:

```bash
cp .env.example .env          # Windows: copy .env.example .env
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

4. Preencha o `.env`. `SUPABASE_KEY` precisa ser uma chave **secreta de backend**.
5. Rode em modo seguro (padrão):

```bash
python main.py
```

Saída esperada: uma linha `[DRY_RUN] Nome (*********1234): Olá, Nome tudo bem com você?` por contato.

6. Envio real, só com contatos autorizados — no `.env`:

```env
DRY_RUN=false
LIVE_SEND_CONFIRM=I_UNDERSTAND
```

Variáveis opcionais (`REQUEST_TIMEOUT`, `SEND_DELAY_SECONDS`, `MAX_ATTEMPTS`, `RETRY_BACKOFF_SECONDS`, `DELIVERY_TABLE`) estão em [`.env.example`](.env.example).

## Testes

```bash
python -m unittest discover -s tests -v
```

Os testes não usam rede: `requests` é substituído por mocks. O CI roda em Python 3.11 e 3.13 e audita as dependências com `pip-audit`.

## Limitações conhecidas

- **Nunca rodou contra Supabase e Z-API reais em ambiente de teste.** Tudo que está verificado está verificado com mocks.
- **Sempre os mesmos três.** A consulta pega os 3 primeiros por `created_at` e não filtra quem já recebeu. Depois que eles recebem, as próximas execuções só pulam — o 4º contato nunca é alcançado.
- **Janela entre enviar e registrar.** Se o envio der certo e a gravação em `deliveries` falhar, a próxima execução manda de novo.
- **`5xx` ainda é repetido.** Um `504` pode significar que a Z-API enviou e só a resposta se perdeu; hoje isso é tratado como falha transitória.
- **Falha não é registrada.** As colunas `status='failed'` e `attempts` existem em `setup.sql`, mas o worker só grava entregas bem-sucedidas. Um erro definitivo interrompe a execução.
- **`DRY_RUN` não consulta `deliveries`.** O modo seguro mostra também quem seria pulado no envio real.

## O que eu aprendi

- **Padrão seguro é decisão de projeto.** Deixar `DRY_RUN=true` por padrão e exigir uma confirmação digitada custa uma linha e elimina o pior erro possível.
- **Idempotência precisa de estado.** Avisar "rode só uma vez" no README não impede nada. Uma chave primária em `deliveries.phone` impede.
- **Nem toda falha pode ser repetida.** Repetir um `429` é correto; repetir depois de um timeout de leitura pode mandar a mensagem duas vezes. A diferença é saber se o pedido chegou ao servidor ([demanda 002](demandas/002-timeout-sem-reenvio/README.md)).
- **Falhar é melhor que duplicar.** Se a tabela de entregas não existe, o worker para em vez de seguir sem controle.
- **Segredo também se protege no código.** Recusar chave `anon` e mascarar telefone no log são verificações pequenas que não dependem de alguém lembrar.

## Estrutura

```text
main.py                 todo o worker
tests/test_main.py      testes com mocks (sem rede)
setup.sql               tabelas, RLS e revogação de acesso público
.env.example            variáveis, sem valores reais
AGENTS.md               regras para quem (pessoa ou agente) for mexer no código
docs/                   histórico, decisões, referências, como foi feito
demandas/               pedidos com especificação, evidência e entrega
.agents/skills/         procedimentos reutilizáveis
```

## Como foi feito

Escrito com apoio de IA generativa, sob minha direção. A divisão do trabalho e o que está ou não verificado: [`docs/como-foi-feito.md`](docs/como-foi-feito.md). O que mudou ao longo do tempo: [`docs/historico.md`](docs/historico.md). Por que cada trava existe: [`docs/decisoes.md`](docs/decisoes.md).
