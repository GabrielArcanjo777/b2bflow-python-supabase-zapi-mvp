---
name: simular-envio
description: Roda o worker em DRY_RUN contra o Supabase configurado e confere o que seria enviado, sem mandar nada.
---

# Simular envio

## Antes

- `.env` existe e tem `DRY_RUN=true` (ou não define `DRY_RUN`).
- **Nunca** altere `DRY_RUN` ou `LIVE_SEND_CONFIRM` nesta skill. Envio real é decisão humana.

## Passos

```bash
grep -E '^DRY_RUN=' .env    # precisa mostrar true, ou nada
python main.py
```

## Saída esperada

```text
DRY_RUN ativo: nenhuma mensagem real será enviada.
[DRY_RUN] Nome (*********1234): Olá, Nome tudo bem com você?
```

Telefone sempre mascarado. Se aparecer um número inteiro na saída, é bug: pare e reporte.

## Limite

O `DRY_RUN` não consulta `deliveries`, então lista também quem seria pulado no envio real.
