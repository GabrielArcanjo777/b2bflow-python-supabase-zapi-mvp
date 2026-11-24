# Timeout de leitura vs. timeout de conexão

O `requests` separa os dois:

| Exceção | O que aconteceu | O pedido chegou? | Repetir é seguro? |
|---|---|---|---|
| `ConnectTimeout` | não conseguiu abrir a conexão | não | sim |
| `ReadTimeout` | conectou, mandou, a resposta não veio a tempo | provavelmente | **não** |
| outras `ConnectionError` | conexão caiu em algum ponto | não dá para saber | não |

O POST para `send-text` não é idempotente: cada chamada que chega vira uma mensagem. Sem um identificador de deduplicação do lado da Z-API, o único jeito seguro de tratar o caso ambíguo é parar e deixar uma pessoa conferir.

A mesma lógica vale para `504 Gateway Timeout`, que continua na lista de retry — fica como próximo passo.
