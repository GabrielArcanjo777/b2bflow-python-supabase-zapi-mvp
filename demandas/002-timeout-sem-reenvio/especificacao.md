# Especificação

## Problema

`send_text_message` tratava qualquer `requests.RequestException` como falha transitória e repetia o POST até `MAX_ATTEMPTS` vezes. Isso inclui `ReadTimeout`, quando a Z-API já recebeu o pedido.

## Objetivo

Nenhuma falha de rede ambígua gera um segundo POST.

## Fora de escopo

- Ambiguidade do `504` (fica registrada em `docs/decisoes.md`, D-005).
- Registrar falhas em `deliveries`.

## Critério de aceite

1. Teste: `ReadTimeout` → 1 chamada a `requests.post`, erro com "resultado desconhecido", sem `sleep`.
2. Teste: `ConnectTimeout` seguido de sucesso → 2 chamadas, sem erro.
3. Os 14 testes anteriores continuam verdes.

## Risco

Uma rede instável passa a parar o worker com mais frequência. É o lado aceitável: parar e conferir é melhor que mandar duas vezes.
