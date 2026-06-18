# Prompts seguros para usar no Codex

## Prompt principal — fazer o projeto completo

Crie um projeto Python para um desafio técnico de estágio.

Objetivo:
Ler contatos cadastrados em uma tabela do Supabase e enviar uma mensagem via Z-API para até 3 contatos.

Requisitos:
- Usar Python.
- Usar Supabase.
- Usar Z-API.
- Ler os contatos da tabela "contacts".
- A tabela deve ter pelo menos: id, nome, telefone.
- Enviar no máximo para 3 contatos.
- A mensagem exata deve ser: "Olá, <nome_contato> tudo bem com você?"
- O campo <nome_contato> deve ser substituído pelo nome vindo do banco.
- Usar variáveis de ambiente com python-dotenv.
- Não deixar chaves expostas no código.
- Criar tratamento básico de erros.
- Criar logs simples no terminal.
- Mascarar telefone nos logs.
- Criar modo DRY_RUN=true por padrão para simular sem enviar mensagens reais.
- Criar README.md curto explicando:
  1. Objetivo do projeto.
  2. Tecnologias usadas.
  3. Como criar a tabela no Supabase.
  4. Quais variáveis colocar no .env.
  5. Como instalar dependências.
  6. Como rodar em modo simulação.
  7. Como enviar de verdade com números autorizados.
- Criar .env.example.
- Criar requirements.txt.
- Criar .gitignore.
- Criar setup.sql.
- Criar COMMITS.md com uma sugestão de commits objetivos.
- Escrever código limpo e fácil de explicar em entrevista.

Restrições de segurança:
- Nunca coloque credenciais reais no código.
- Nunca coloque números reais no README.
- Nunca suba .env.
- Use apenas dados fictícios no setup.sql.
- Não crie frontend, pois as credenciais da Z-API devem ficar no backend/local.
- Não registre telefone completo nos logs.

## Prompt — revisar e melhorar o README

Revise e melhore o README.md deste projeto.

Quero um README profissional, curto e direto, com:
- Nome do projeto.
- Objetivo.
- Tecnologias usadas.
- Estrutura de arquivos.
- Setup da tabela no Supabase.
- Variáveis de ambiente.
- Como instalar dependências.
- Como rodar com DRY_RUN=true.
- Como enviar de verdade com DRY_RUN=false.
- Cuidados de segurança: não subir .env, não usar dados reais, usar apenas números próprios/autorizados.
- Observação de que é um MVP técnico para processo seletivo.

Não use linguagem exagerada de marketing.
Não invente funcionalidades que o código não possui.
Não coloque credenciais reais.
Não coloque número real.

## Prompt — fazer commits objetivos

Analise o projeto atual e faça commits pequenos, objetivos e profissionais.

Antes de commitar:
- Verifique se o arquivo .env não está versionado.
- Verifique se .gitignore ignora .env.
- Verifique se não existem credenciais reais em nenhum arquivo.
- Verifique se não existem números pessoais/reais em README.md ou setup.sql.
- Rode uma revisão rápida do código.

Faça os commits nesta ordem, se as mudanças existirem:

1. chore: configura estrutura inicial do projeto
2. feat: integra leitura de contatos no Supabase
3. feat: adiciona envio de mensagens via Z-API
4. safety: adiciona dry run e proteção de credenciais
5. docs: documenta setup e execução do projeto
6. docs: adiciona guia de commits

Regras:
- Não faça um commit gigante se puder separar por assunto.
- Mensagens de commit devem ser curtas e claras.
- Não inclua .env nos commits.
- Não inclua chaves, tokens ou dados reais.
- Não force push.
- Não altere o escopo do desafio.

## Prompt — checagem final antes de subir no GitHub

Faça uma checagem final do repositório antes de publicar no GitHub.

Verifique:
- .env não está no Git.
- .env.example existe e não contém segredo real.
- README explica como rodar.
- setup.sql usa apenas dados fictícios.
- Código limita o envio a no máximo 3 contatos.
- DRY_RUN=true é o padrão recomendado.
- Logs não expõem telefone completo.
- requirements.txt tem as dependências necessárias.
- Projeto roda com python main.py.

Depois, gere um resumo curto do que foi validado e diga se está pronto para publicar.
