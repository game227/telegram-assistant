import asyncpg

SCHEMA = """
CREATE TABLE IF NOT EXISTS messages (
    id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    image_path TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_messages_chat_id_created_at
    ON messages (chat_id, created_at);

CREATE TABLE IF NOT EXISTS pending_approvals (
    id BIGSERIAL PRIMARY KEY,
    kind TEXT NOT NULL CHECK (kind IN ('auto_reply', 'send_on_behalf')),
    target TEXT NOT NULL,
    target_display_name TEXT,
    original_message TEXT,
    instruction TEXT,
    draft_text TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'approved', 'rejected', 'sent', 'edited')),
    bot_chat_id BIGINT,
    bot_message_id BIGINT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS reminders (
    id BIGSERIAL PRIMARY KEY,
    owner_chat_id BIGINT NOT NULL,
    text TEXT NOT NULL,
    run_at TIMESTAMPTZ NOT NULL,
    recurring TEXT,
    apscheduler_job_id TEXT,
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'sent', 'cancelled')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS news_seen (
    id BIGSERIAL PRIMARY KEY,
    feed_url TEXT NOT NULL,
    entry_id TEXT NOT NULL,
    title TEXT,
    published_at TIMESTAMPTZ,
    seen_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (feed_url, entry_id)
);

CREATE TABLE IF NOT EXISTS contact_aliases (
    id BIGSERIAL PRIMARY KEY,
    alias TEXT NOT NULL UNIQUE,
    telegram_username_or_id TEXT NOT NULL,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""

CONTEXT_WINDOW_SIZE = 20


async def init_pool(database_url: str) -> asyncpg.Pool:
    pool = await asyncpg.create_pool(database_url, min_size=1, max_size=5)
    async with pool.acquire() as conn:
        await conn.execute(SCHEMA)
    return pool


async def add_message(
    pool: asyncpg.Pool, chat_id: int, role: str, content: str, image_path: str | None = None
) -> None:
    await pool.execute(
        "INSERT INTO messages (chat_id, role, content, image_path) VALUES ($1, $2, $3, $4)",
        chat_id, role, content, image_path,
    )


async def get_recent_messages(
    pool: asyncpg.Pool, chat_id: int, limit: int = CONTEXT_WINDOW_SIZE
) -> list[dict]:
    rows = await pool.fetch(
        """
        SELECT role, content FROM (
            SELECT role, content, created_at FROM messages
            WHERE chat_id = $1
            ORDER BY created_at DESC
            LIMIT $2
        ) recent
        ORDER BY created_at ASC
        """,
        chat_id, limit,
    )
    return [{"role": row["role"], "content": row["content"]} for row in rows]
