---
name: verificar
description: Roda a mesma checagem do CI (sintaxe, testes, auditoria de dependências) antes de declarar uma mudança pronta.
---

# Verificar

```bash
bash .agents/skills/verificar/scripts/verificar.sh
```

Roda `compileall`, os testes e, se `pip-audit` estiver instalado, a auditoria de dependências. Para no primeiro erro.

Os testes não usam rede nem `.env`: tudo é mock. Se um teste precisar de credencial real, ele está errado.

**Pronto quando:** termina com `OK: tudo verde`.
