# Entregáveis

| Arquivo | Mudança |
|---|---|
| `main.py` | `ConnectTimeout` é repetido; outra `RequestException` levanta `RuntimeError` com "resultado desconhecido" |
| `tests/test_main.py` | `test_read_timeout_is_not_retried`, `test_connect_timeout_is_retried` |

Commit: `fix: nao repete envio depois de timeout de leitura`.

## Verificação

- `python -m unittest discover -s tests -v` → 16 testes, OK.
- `python -m compileall -q main.py tests` → sem erro.
