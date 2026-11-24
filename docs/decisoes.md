# Decisões

Registro curto do que foi decidido e por quê. Não reescreva uma decisão antiga: adicione uma nova que a substitua.

---

## D-001 — `DRY_RUN=true` por padrão e confirmação digitada para envio real

**Por quê:** o pior erro possível é mandar mensagem real sem querer. Uma variável a mais no `.env` custa nada.

**Consequência:** valor inválido em `DRY_RUN` (ex.: `ture`) para a execução em vez de cair em algum padrão.

---

## D-002 — Supabase via REST com chave secreta; RLS ligado

**Por quê:** a tabela tem telefone. Chave `anon`/`publishable` vai parar em front-end; com ela e sem RLS, qualquer um lê os contatos.

**Consequência:** o worker recusa chave `anon` e `sb_publishable_*`. `setup.sql` liga RLS e revoga `anon`/`authenticated`.

---

## D-003 — Idempotência por telefone na tabela `deliveries`

**Por quê:** "rode só uma vez" é instrução para humano. A chave primária em `phone` é garantia do banco.

**Consequência:** se `deliveries` não existe, o worker para (HTTP 404 → erro) em vez de enviar sem controle. Substitui a nota antiga do `AGENTS.md` que dizia não haver controle de reenvio.

**Limite aceito:** se o envio der certo e a gravação falhar, a próxima execução reenvia.

---

## D-004 — Retry só no que é seguro repetir

**Por quê:** `429` e `503` querem dizer "tente depois". `400` quer dizer "pedido errado" — repetir só aumenta o risco de bloqueio do número.

**Consequência:** retry com backoff exponencial em `408, 425, 429, 500, 502, 503, 504`. `4xx` restante para na hora.

---

## D-005 — Timeout de leitura não é repetido (substitui parte da D-004)

**Por quê:** num timeout de leitura o pedido chegou à Z-API e a mensagem pode ter saído. Repetir pode mandar duas vezes — exatamente o que a D-003 tenta evitar. Num timeout de conexão o pedido não chegou, então repetir é seguro.

**Consequência:** `ConnectTimeout` é repetido; qualquer outra falha de rede para o worker com "resultado desconhecido" e pede conferência humana.

**Em aberto:** `504` tem a mesma ambiguidade e ainda é repetido. Ver limitações no README.
