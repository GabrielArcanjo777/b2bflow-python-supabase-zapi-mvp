# Histórico

O que já foi feito, tirado do `git log`. Para o porquê, ver [`decisoes.md`](decisoes.md).

## 18/jun/2026 — MVP

- `36628be` estrutura inicial
- `16d5297` leitura de contatos no Supabase (REST, sem SDK)
- `d5e3d29` envio via Z-API
- `f239dc6` `DRY_RUN` e credenciais só por variável de ambiente
- `29ed20e` telefone repetido é ignorado antes do envio
- `4626ba5` arquivos internos removidos do repositório público

## 12/jul/2026 — Fail-closed (PR #2)

- `a2c8bc8` envio real passa a exigir `LIVE_SEND_CONFIRM=I_UNDERSTAND`; valor inválido em `DRY_RUN` para a execução; chave `anon`/`publishable` recusada; RLS e revogação de acesso público no `setup.sql`; CI em Python 3.11 e 3.13 com `pip-audit`; Dependabot.

## 17/nov/2026 — Agentes e idempotência

- `95958b7` `AGENTS.md` e demanda 001 (reenvio e retry)
- `e4a00fe`, `bd2ebdb` declaração de uso de IA e do que está verificado
- `edf4d49` tabela `deliveries` impede reenvio; retry com backoff exponencial em `408/425/429/5xx`

## 23/nov/2026 — Timeout sem reenvio

- Demanda [002](../demandas/002-timeout-sem-reenvio/README.md): o retry repetia o POST depois de timeout de **leitura**, quando a mensagem pode já ter saído. Agora só timeout de **conexão** é repetido. Dois testes novos (16 no total).
- `.env.example` ganhou as variáveis de retry e de entregas, que o README já citava.
- README reescrito com fluxo, travas, limitações conhecidas e o que eu aprendi.
- `AGENTS.md` deixou de dizer que não havia controle de reenvio nem retry (ambos existem desde `edf4d49`).
- Estrutura: `docs/`, `demandas/<id>/`, `.agents/skills/`.
