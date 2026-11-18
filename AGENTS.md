# AGENTS.md

> Leia antes de alterar qualquer arquivo.

## Contexto

**O que é:** worker em Python que lê contatos autorizados de uma tabela no Supabase e envia uma mensagem personalizada via Z-API (WhatsApp não oficial).

**O que não é:** produto, disparador em massa, ferramenta de marketing. Não existe cadastro de usuário, fila, nem histórico de entrega.

**Regra cardinal:** `DRY_RUN=true` é o padrão. Envio real exige `DRY_RUN=false` **e** `LIVE_SEND_CONFIRM=I_UNDERSTAND`. Nenhuma mudança pode afrouxar isso.

**Dado sensível:** telefone. Só contatos fictícios, próprios ou explicitamente autorizados entram em código, teste ou documentação.

## Responsabilidades

**Pode:**
- corrigir bugs, ampliar testes, refatorar
- melhorar tratamento de erro e logging
- atualizar documentação e este arquivo

**Não pode:**
- remover o gate de envio real
- commitar `.env` ou qualquer telefone real
- usar chave `anon`/`publishable` do Supabase para ler contatos
- desligar RLS

**Escala para humano quando:**
- a mudança toca credencial, RLS ou gate de envio
- entra dependência nova

## Requisitos de entrega

- `python -m unittest discover -s tests -v` verde
- `python -m compileall -q main.py tests` sem erro
- CI verde nas duas versões de Python (3.11 e 3.13)
- teste novo para comportamento novo

## Skills

| Skill | Comando |
|---|---|
| Rodar | `python main.py` |
| Testar | `python -m unittest discover -s tests -v` |
| Sintaxe | `python -m compileall -q main.py tests` |
| Auditar deps | `python -m pip_audit -r requirements.txt` |

## Decisões

- SQLite local não é usado: o estado é o Supabase. Consequência: **não há controle de reenvio**.
- `requests` síncrono, sem retry. Consequência: falha de rede perde a mensagem.
- Nenhuma mensagem é enviada sem `DRY_RUN=false` + confirmação explícita.
