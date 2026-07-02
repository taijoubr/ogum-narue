# Centro Espírita Ogum Naruê

Site institucional desenvolvido com Flask e Jinja2.

## Como executar

1. Crie um ambiente virtual.
2. Instale as dependências:
   `pip install -r requirements.txt`
3. Execute:
   `python app.py`

## Rotas disponíveis

- `/`
- `/historia`
- `/agenda`
- `/nossa-casa`
- `/faq`
- `/contato`

## Painel Administrativo (Fase 3) — Supabase / Tabela de Auditoria

Para integrar o painel administrativo com o Supabase (Postgres) crie a tabela de auditoria no seu projeto Supabase.

Opções para criar a tabela:

- Pelo editor SQL do Supabase (Dashboard → SQL Editor): cole o conteúdo de `sql/create_audit_table.sql` e execute.
- Via `psql` local (usando `DATABASE_URL`):

```bash
# export DATABASE_URL or set in PowerShell
psql "$DATABASE_URL" -f sql/create_audit_table.sql
```

Conteúdo da tabela (resumo):

- `id` (BIGSERIAL) — chave primária
- `usuario` (VARCHAR) — usuário que executou a ação
- `acao` (VARCHAR) — ação realizada
- `descricao` (TEXT) — informações adicionais
- `ip` (VARCHAR) — endereço IP
- `data` (TIMESTAMPTZ) — timestamp com timezone (default agora)

Recomendações:

- Use a `Service Role` key somente no backend (variável de ambiente no Vercel).
- Para aplicações que usam RLS, prefira `supabase-py` com políticas adequadas.
- Após criar a tabela, você pode usar o serviço local `services/audit_service.py` para gravar auditoria localmente e replicar para Supabase (o projeto já contém `services/supabase_service.py`).

## Integração de Login Administrativo com Supabase

O painel administrativo agora suporta autenticação via Supabase Auth quando `SUPABASE_URL` e `SUPABASE_KEY` estiverem configurados.

Variáveis de ambiente recomendadas:

- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SUPABASE_ADMIN_EMAILS` (ex: `admin@example.com`)
- `SUPABASE_PROGRAMADOR_EMAILS` (ex: `dev@example.com`)
- `SUPABASE_SECRETARIA_EMAILS`
- `SUPABASE_TESOURARIA_EMAILS`

Se nenhuma lista de e-mails de função estiver configurada, qualquer usuário Supabase autenticado terá acesso como `ADMINISTRADOR`.

O fallback local continua disponível com:

- `ADMIN_USER`
- `ADMIN_PASS`

Isso permite usar Supabase como backend de autenticação sem perder a compatibilidade de desenvolvimento local.

### Exemplo PowerShell

No PowerShell, exporte as variáveis de ambiente antes de executar o Flask:

```powershell
$env:SUPABASE_URL = "https://your-project.supabase.co"
$env:SUPABASE_KEY = "your-service-role-key"
$env:SUPABASE_ADMIN_EMAILS = "admin@example.com"
$env:ADMIN_USER = "admin"
$env:ADMIN_PASS = "admin"
python app.py
```

Se você usa o fallback local, basta colocar `ADMIN_USER` e `ADMIN_PASS` no ambiente.

Se quiser, eu posso executar a criação da tabela diretamente se você fornecer `DATABASE_URL` temporariamente, ou você pode rodar o comando no painel do Supabase agora.

