# Como foi feito

## Declaração

Este projeto foi desenvolvido com **agentes de IA**, sob minha direção. Eu defini o problema e as regras de segurança; os agentes implementaram boa parte do código.

É um **projeto de estudo** — o objetivo é aprender integração entre serviços, tratamento de erro e postura defensiva ao lidar com dado sensível, não operar um disparador de mensagens.

## Divisão do trabalho

**Eu:**
- defini o objetivo: ler contatos autorizados e enviar uma mensagem personalizada com trava de segurança
- decidi que `DRY_RUN=true` seria o padrão e que envio real exigiria confirmação digitada
- exigi RLS no Supabase e revogação dos papéis públicos
- decidi que telefone sairia mascarado nos logs
- revisei a documentação

**Agentes:**
- implementaram a leitura de contatos, o envio, os testes e o tratamento de variáveis de ambiente
- propuseram as proteções a partir dos requisitos que eu passei

## O que está verificado

| Verificação | Como |
|---|---|
| Testes | `python -m unittest discover -s tests -v`, local e no CI |
| Sintaxe | `python -m compileall -q main.py tests` |
| Dependências | `pip-audit`, no CI |
| Compatibilidade | Python 3.11 e 3.13, no CI |

## O que ainda não está verificado

- nenhuma execução real contra o Supabase ou a Z-API em ambiente de teste
- nenhum teste de carga
- nenhuma revisão de código por terceiros

## Conclusão

Projeto pequeno, feito para estudar. As travas de segurança (`DRY_RUN`, confirmação explícita, RLS, log mascarado) são o que interessa aqui — o envio em si é a parte trivial.
