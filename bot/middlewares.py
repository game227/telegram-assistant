from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User


class OwnerOnlyMiddleware(BaseMiddleware):
    """Botni faqat OWNER_TELEGRAM_USER_ID bilan cheklaydi, boshqalarni jimgina e'tiborsiz qoldiradi."""

    def __init__(self, owner_id: int) -> None:
        self.owner_id = owner_id

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: User | None = data.get("event_from_user")
        if user is None or user.id != self.owner_id:
            return None
        return await handler(event, data)
