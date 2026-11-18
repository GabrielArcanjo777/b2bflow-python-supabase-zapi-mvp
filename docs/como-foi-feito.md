# Como foi feito

## Declaração de uso de IA

Este projeto foi escrito com apoio de IA generativa. Está escrito aqui, no repositório, em vez de aparecer como surpresa numa conversa.

## Divisão do trabalho

**Humano (eu):**
- defini o problema: ler contatos autorizados e enviar uma mensagem personalizada, com trava de segurança
- decidi que `DRY_RUN=true` seria o padrão e que envio real exigiria confirmação digitada
- escolhi exigir RLS no Supabase e revogar os papéis públicos da tabela
- decidi que telefone apareceria mascarado nos logs
- escrevi e revisei a documentação

**IA:**
- escreveu a maior parte do código
- propôs a estrutura de módulos, os testes e o tratamento de variável de ambiente
- sugeriu as proteções de segurança a partir do meu pedido

## O que está verificado

| Verificação | Como |
|---|---|
| Testes | `python -m unittest discover -s tests -v`, local e no CI |
| Sintaxe | `python -m compileall -q main.py tests` |
| Dependências | `pip-audit`, no CI |
| Compatibilidade | Python 3.11 e 3.13, no CI |

## O que não está verificado

- nenhuma execução real contra o Supabase ou a Z-API em ambiente de teste
- nenhum teste de carga
- nenhum reenvio controlado — **o script não sabe se já mandou** (ver `demandas/001-idempotencia-e-retry.md`)
- nenhuma revisão de código por terceiros

## Consequência

Use com contatos próprios ou explicitamente autorizados. Não use em disparo em massa. O controle de duplicidade é humano, não do sistema — isso é uma limitação conhecida, não um bug escondido.
