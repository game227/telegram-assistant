import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import ai
import db
from bot.handlers import chat as chat_handler
from bot.handlers import start as start_handler
from bot.middlewares import OwnerOnlyMiddleware
from config import load_settings
from context import AppContext


async def main() -> None:
    settings = load_settings()
    logging.basicConfig(level=settings.log_level)

    bot = Bot(
        token=settings.telegram_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    pool = await db.init_pool(settings.database_url)
    anthropic_client = ai.make_client(settings.anthropic_api_key)

    ctx = AppContext(bot=bot, settings=settings, db=pool, anthropic_client=anthropic_client)
    dp.workflow_data["ctx"] = ctx

    owner_only = OwnerOnlyMiddleware(settings.owner_telegram_user_id)
    dp.message.outer_middleware(owner_only)
    dp.callback_query.outer_middleware(owner_only)

    dp.include_router(start_handler.router)
    dp.include_router(chat_handler.router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await pool.close()


if __name__ == "__main__":
    asyncio.run(main())
