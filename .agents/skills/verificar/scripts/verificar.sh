#!/usr/bin/env bash
# Mesma verificação do job de CI.
set -euo pipefail
cd "$(dirname "$0")/../../../.."

echo "== sintaxe"
python -m compileall -q main.py tests
echo "== testes"
python -m unittest discover -s tests -v
if python -m pip_audit --version >/dev/null 2>&1; then
  echo "== pip-audit"
  python -m pip_audit -r requirements.txt
else
  echo "== pip-audit não instalado (pip install pip-audit); o CI roda essa etapa"
fi

echo "OK: tudo verde"
