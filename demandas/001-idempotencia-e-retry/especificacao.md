# 001 — Idempotência e retry no envio

**Estado:** aberta · **Aberta em:** 2026-11-17

## Problema

Duas falhas reais, ambas já confessadas no README:

1. **Não há controle de reenvio.** Se o script rodar duas vezes, o mesmo contato recebe a mensagem de novo. O README avisa "execute o envio real apenas uma vez" — isso é instrução para humano, não garantia de sistema.
2. **Não há retry.** `requests` síncrono, uma tentativa. Um 429 ou timeout da Z-API perde a mensagem silenciosamente.

## Objetivo

O worker pode ser executado mais de uma vez sem duplicar mensagem, e uma falha transitória da Z-API não perde o envio.

## Critério de aceite

1. Tabela `public.deliveries` criada por `setup.sql`, com `contact_id`, `sent_at`, `status`, `attempts` e chave única em `contact_id`.
2. Contato com entrega `sent` é pulado na execução seguinte.
3. Retry com backoff exponencial em `429`, `5xx` e timeout — máximo configurável por `MAX_ATTEMPTS`.
4. Teste cobrindo: reenvio bloqueado, retry em 429, falha definitiva registrada.
5. `DRY_RUN` continua não gravando entrega.

## Fora de escopo

- fila assíncrona
- migrar para WhatsApp Cloud API

## Risco

A tabela nova precisa de RLS igual à de contatos. Um erro aqui expõe telefone.
