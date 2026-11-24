# 001 — Idempotência e retry no envio

**Estado:** entregue em `edf4d49` (17/nov/2026), com diferenças em relação à especificação.

- Especificação original: [`especificacao.md`](especificacao.md)

## O que ficou diferente

| Critério | Resultado |
|---|---|
| 1. `deliveries` com chave única em `contact_id` | chave em `phone` — o worker não lê o `id` do contato, e telefone é o que não pode receber duas vezes |
| 2. contato `sent` é pulado | feito, com teste |
| 3. retry com backoff em `429`, `5xx` e timeout | feito; o retry em timeout foi corrigido na [002](../002-timeout-sem-reenvio/README.md) |
| 4. teste de "falha definitiva registrada" | **não feito**: falha interrompe a execução e não é gravada |
| 5. `DRY_RUN` não grava entrega | feito |
