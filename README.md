# telegram-assistant

Shaxsiy Telegram yordamchi bot: Claude (Anthropic API) yordamida foydalanuvchi bilan o'zbek tilida suhbatlashadi. Faqat egasi (`OWNER_TELEGRAM_USER_ID`) foydalana oladi.

## Stack
aiogram 3 · Telethon (userbot, keyingi faza) · Anthropic SDK · APScheduler · feedparser · PostgreSQL (asyncpg)

## Tuzilma
- `main.py` — kirish nuqtasi (bot, DB pool, Claude klienti)
- `bot/` — aiogram handlerlar (`start`, `chat`) va owner-only middleware
- `ai.py` — Claude klienti va system prompt
- `skills/` — kelajakdagi ko'nikmalar: `news_digest`, `reminders`, `send_on_behalf` (hozircha bo'sh)
- `userbot/` — Telethon userbot (hozircha bo'sh)
- `db.py`, `config.py`, `context.py` — ma'lumotlar bazasi, sozlamalar, umumiy kontekst

## Ishga tushirish
```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env   # tokenlarni to'ldiring
./start_bot.sh
```

## Holat
Faza 1: suhbat boti ishlaydi. Skills va userbot hali yozilmagan.
`.env`, sessiya fayllari va loglar `.gitignore` orqali commit'dan chiqarilgan.
