# Guia de commits

Sequência sugerida para manter o histórico pequeno, objetivo e fácil de explicar em uma revisão técnica.

## 1. Estrutura inicial

**Commit**

```bash
git commit -m "chore: configura estrutura inicial do projeto"
```

**Inclui**

- `.gitignore`
- `.env.example`
- `requirements.txt`
- `setup.sql`

**Objetivo**

Criar a base do MVP sem credenciais reais, com `.env` ignorado e tabela documentada no SQL.

## 2. Leitura de contatos no Supabase

**Commit**

```bash
git commit -m "feat: integra leitura de contatos no Supabase"
```

**Inclui**

- `main.py`

**Objetivo**

Ler até três contatos da tabela `contacts` usando as variáveis `SUPABASE_URL`, `SUPABASE_KEY` e `SUPABASE_TABLE`.

## 3. Envio via Z-API

**Commit**

```bash
git commit -m "feat: adiciona envio de mensagens via Z-API"
```

**Inclui**

- `main.py`

**Objetivo**

Adicionar a função de envio de mensagem pela Z-API usando credenciais carregadas do ambiente.

## 4. Segurança e dry run

**Commit**

```bash
git commit -m "safety: adiciona dry run e proteção de credenciais"
```

**Inclui**

- `main.py`
- `.env.example`

**Objetivo**

Ativar `DRY_RUN=true` por padrão, limitar o envio a no máximo três contatos, mascarar telefones nos logs e evitar mensagens de erro que exponham tokens.

## 5. README

**Commit**

```bash
git commit -m "docs: documenta setup e execução do projeto"
```

**Inclui**

- `README.md`

**Objetivo**

Explicar objetivo, tecnologias, setup do Supabase, variáveis de ambiente, instalação, execução em simulação e envio real com contatos autorizados.

## 6. Guia de commits

**Commit**

```bash
git commit -m "docs: adiciona guia de commits"
```

**Inclui**

- `COMMITS.md`
- `PROMPTS_CODEX.md`, se o arquivo fizer parte da entrega

**Objetivo**

Documentar o histórico recomendado e registrar prompts seguros usados para orientar a criação do MVP.

## Checagens antes do push

Confirme que o `.env` não está versionado:

```bash
git ls-files .env
```

O comando não deve retornar nada.

Confirme que `.env.example` é o arquivo de exemplo versionado:

```bash
git ls-files .env.example
```

Confirme que `.env` é ignorado:

```bash
git check-ignore -v .env
```

Revise o histórico:

```bash
git log --oneline
```

Antes de publicar, verifique também:

- Não existem chaves, tokens ou dados pessoais nos arquivos do projeto.
- `README.md` e `setup.sql` não contêm telefones reais.
- O projeto continua limitado ao MVP técnico.
- Não foi usado `git push --force`.
