# AGENTS.md

> Leia antes de alterar qualquer arquivo.

## Contexto

**O que é:** worker em Python que lê contatos autorizados de uma tabela no Supabase e envia uma mensagem personalizada via Z-API (WhatsApp não oficial).

**O que não é:** produto, disparador em massa, ferramenta de marketing. Não existe cadastro de usuário nem fila. O único estado é a tabela `deliveries` (quem já recebeu).

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
- linha em `docs/historico.md`; entrada em `docs/decisoes.md` se mudar uma trava

**Pronto** = código + teste + doc + CI verde.

## Skills

Procedimentos com passo a passo em `.agents/skills/`:

| Skill | Para quê |
|---|---|
| [`verificar`](.agents/skills/verificar/SKILL.md) | mesma checagem do CI antes de abrir PR |
| [`simular-envio`](.agents/skills/simular-envio/SKILL.md) | rodar em `DRY_RUN` e conferir a saída sem tocar em número real |

## Dados

Não há pasta `dados/`: os contatos vivem no Supabase do usuário e **nunca** entram no repositório. Testes usam telefones fictícios (`5521999990000`).

## Onde está cada coisa

| Preciso de | Vá para |
|---|---|
| Visão geral e como rodar | `README.md` |
| O que já foi feito | `docs/historico.md` |
| Por que foi feito assim | `docs/decisoes.md` |
| Como foi produzido | `docs/como-foi-feito.md` |
| Documentação externa | `docs/referencias.md` |
| Pedidos e backlog | `demandas/` |
