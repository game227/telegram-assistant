import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    telegram_api_id: str | None
    telegram_api_hash: str | None
    telegram_phone: str | None
    anthropic_api_key: str | None
    claude_model: str
    owner_telegram_user_id: int
    database_url: str
    session_path: str
    timezone: str
    news_digest_hour: int
    log_level: str


def _get_int(name: str) -> int | None:
    value = os.getenv(name)
    return int(value) if value else None


def load_settings() -> Settings:
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN yo'q. .env faylini .env.example asosida to'ldiring."
        )

    owner_id = _get_int("OWNER_TELEGRAM_USER_ID")
    if owner_id is None:
        raise RuntimeError(
            "OWNER_TELEGRAM_USER_ID yo'q. Bot faqat egasiga cheklanishi uchun bu shart."
        )

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL yo'q. .env faylini .env.example asosida to'ldiring."
        )

    return Settings(
        telegram_bot_token=bot_token,
        telegram_api_id=os.getenv("TELEGRAM_API_ID"),
        telegram_api_hash=os.getenv("TELEGRAM_API_HASH"),
        telegram_phone=os.getenv("TELEGRAM_PHONE"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        claude_model=os.getenv("CLAUDE_MODEL", "claude-sonnet-5"),
        owner_telegram_user_id=owner_id,
        database_url=database_url,
        session_path=os.getenv("SESSION_PATH", "data/userbot"),
        timezone=os.getenv("TIMEZONE", "Asia/Tashkent"),
        news_digest_hour=int(os.getenv("NEWS_DIGEST_HOUR", "9")),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )
