from config import OPENAI_API_KEY
import aiohttp
import asyncio

MAX_CHARS = 500

async def ai_reply(text: str) -> str:
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + "❌ The message is too long. Please shorten the text."
        
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    json_data = {
        "model": "upstage/solar-pro-3:free",
        "messages": [
            {"role": "system", "content": "Ты помощник бизнеса. Отвечай кратко и по делу."},
            {"role": "user", "content": text},
        ],
        "max_tokens": 500,
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=json_data
        ) as resp:
            data = await resp.json()
            reply = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return reply.strip() if reply else "Sorry, AI couldn't provide an answer."