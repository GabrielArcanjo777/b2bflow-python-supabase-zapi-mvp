# Antes da correção

Trecho de `main.py` (commit `edf4d49`):

```python
try:
    response = requests.post(url, headers=headers, json=payload, timeout=timeout)
except requests.RequestException as exc:
    last_error = f"falha de rede ({type(exc).__name__})"
```

Teste novo rodando contra esse código:

```text
FAIL: test_read_timeout_is_not_retried (tests.test_main.RetryTests.test_read_timeout_is_not_retried)
RuntimeError: Falha ao enviar mensagem pela Z-API após 3 tentativa(s): falha de rede (ReadTimeout).
```

Três tentativas = três POSTs = até três mensagens para o mesmo contato.
