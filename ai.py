from anthropic import AsyncAnthropic

SYSTEM_PROMPT = (
    "Sen foydalanuvchining shaxsiy Telegram yordamchisisan. "
    "Foydalanuvchi bilan o'zbek tilida (yoki u yozgan tilda), qisqa, aniq va do'stona javob ber. "
    "Agar savol tushunarsiz bo'lsa, aniqlashtirib so'ra."
)


def make_client(api_key: str) -> AsyncAnthropic:
    return AsyncAnthropic(api_key=api_key)


async def chat(client: AsyncAnthropic, model: str, history: list[dict], user_message: str) -> str:
    messages = history + [{"role": "user", "content": user_message}]
    response = await client.messages.create(
        model=model,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages,
    )
    return "".join(block.text for block in response.content if block.type == "text")
