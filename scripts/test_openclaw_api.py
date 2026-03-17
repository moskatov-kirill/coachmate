#!/usr/bin/env python
"""
Тестирование API OpenClaw
"""
import asyncio
import os

import aiohttp
from dotenv import load_dotenv

load_dotenv()


async def test_openclaw():
    print("🚀 Тестирование OpenClaw API...")

    async with aiohttp.ClientSession() as session:
        # Проверяем, что OpenClaw отвечает
        try:
            async with session.get("http://localhost:18789/health") as resp:
                if resp.status == 200:
                    print("✅ OpenClaw доступен")
                else:
                    print(f"❌ OpenClaw вернул статус {resp.status}")
                    return
        except Exception as e:
            print(f"❌ OpenClaw не отвечает: {e}")
            return

        # Тестируем обработку сообщения
        payload = {"user_id": "test_user_123", "message": "Привет!", "platform": "vk"}

        try:
            async with session.post(
                "http://localhost:18789/api/process", json=payload, timeout=10
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print(f"✅ OpenClaw обработал запрос")
                    print(f"   Ответ: {data.get('response', 'нет ответа')[:50]}...")
                else:
                    print(f"❌ Ошибка обработки: {resp.status}")
        except Exception as e:
            print(f"❌ Ошибка при запросе: {e}")


if __name__ == "__main__":
    asyncio.run(test_openclaw())
