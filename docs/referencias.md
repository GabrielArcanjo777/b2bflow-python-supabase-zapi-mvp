# Referências

- [Supabase — REST API (PostgREST)](https://supabase.com/docs/guides/api) — leitura e upsert sem SDK.
- [PostgREST — upsert com `on_conflict`](https://docs.postgrest.org/en/stable/references/api/tables_views.html#upsert) — usado em `mark_delivered`.
- [Supabase — Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security) — base do `setup.sql`.
- [Supabase — chaves de API](https://supabase.com/docs/guides/api/api-keys) — diferença entre chave publishable e secreta.
- [Z-API — enviar texto](https://developer.z-api.io/message/send-message-text) — endpoint `send-text` e header `Client-Token`.
- [Requests — exceções](https://requests.readthedocs.io/en/latest/api/#exceptions) — `ConnectTimeout` vs `ReadTimeout` (D-005).
- [MDN — códigos HTTP](https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status) — quais são transitórios (D-004).
- [pip-audit](https://github.com/pypa/pip-audit) — auditoria de dependências no CI.
