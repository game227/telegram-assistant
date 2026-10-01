from dataclasses import dataclass
from typing import Any

from aiogram import Bot

from config import Settings


@dataclass
class AppContext:
    """Ilova bo'ylab bo'lishiladigan umumiy obyektlar (bot, db, ai, userbot...).

    Keyingi fazalarda db/anthropic_client/telethon_client shu yerga qo'shiladi.
    """

    bot: Bot
    settings: Settings
    db: Any = None
    anthropic_client: Any = None
    telethon_client: Any = None
