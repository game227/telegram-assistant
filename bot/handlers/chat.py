from aiogram import F, Router
from aiogram.types import Message

import db
from ai import chat as ai_chat
from context import AppContext

router = Router(name="chat")


@router.message(F.text)
async def handle_text(message: Message, ctx: AppContext) -> None:
    chat_id = message.chat.id
    user_text = message.text

    await ctx.bot.send_chat_action(chat_id, "typing")

    history = await db.get_recent_messages(ctx.db, chat_id)
    reply_text = await ai_chat(ctx.anthropic_client, ctx.settings.claude_model, history, user_text)

    await db.add_message(ctx.db, chat_id, "user", user_text)
    await db.add_message(ctx.db, chat_id, "assistant", reply_text)

    await message.answer(reply_text)
