from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Salom! Men sizning shaxsiy Telegram yordamchingizman.\n"
        "Hozircha ishga tushirish bosqichidaman — tez orada AI suhbat, "
        "eslatmalar va boshqa funksiyalar qo'shiladi."
    )
