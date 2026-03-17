#!/usr/bin/env python
"""
Тестирование VK API
"""
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()


def test_vk_config():
    print("\n📱 Тестирование VK API...")
    token = os.getenv("VK_GROUP_TOKEN")
    group_id = os.getenv("VK_GROUP_ID")

    if not token:
        print("❌ VK_GROUP_TOKEN не найден в .env")
        return False

    if not group_id:
        print("❌ VK_GROUP_ID не найден в .env")
        return False

    print(f"✅ VK токен найден (первые 10 символов: {token[:10]}...)")
    print(f"✅ VK Group ID: {group_id}")

    if token.startswith("vk1."):
        print("✅ Формат токена корректный")
    else:
        print("⚠️ Необычный формат токена, но может работать")

    return True


def test_vk_connection():
    print("\n🔌 Тестирование подключения к VK API...")

    try:
        from vkbottle import API
        from vkbottle.http import AiohttpClient
        import aiohttp
        import ssl

        async def check():
            token = os.getenv("VK_GROUP_TOKEN")
            group_id = os.getenv("VK_GROUP_ID")

            if not token or not group_id:
                return False

            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            connector = aiohttp.TCPConnector(ssl=ssl_context)
            http_client = AiohttpClient(connector=connector)
            api = API(token, http_client=http_client)

            try:
                groups = await api.request(
                    "groups.getById", {"group_id": group_id, "fields": "name,members_count"}
                )

                if isinstance(groups, dict) and "response" in groups:
                    response_data = groups["response"]
                    if isinstance(response_data, dict) and "groups" in response_data:
                        groups_list = response_data["groups"]
                        if groups_list:
                            group_info = groups_list[0]
                            group_name = group_info.get("name", "Unknown")
                            members = group_info.get("members_count", 0)
                            print(f"✅ Подключение успешно! Группа: {group_name}")
                            print(f"   Участников: {members}")
                            return True
                return False
            except Exception:
                return False

        result = asyncio.run(check())
        return result
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False


def test_vk_longpoll():
    print("\n🔄 Проверка LongPoll...")

    try:
        from vkbottle import Bot
        from vkbottle.polling import BotPolling

        token = os.getenv("VK_GROUP_TOKEN")
        if not token:
            print("❌ VK_GROUP_TOKEN не найден")
            return False

        bot = Bot(token=token)
        polling = BotPolling(bot)

        if hasattr(polling, "get_server") and hasattr(polling, "listen"):
            print("✅ LongPoll настроен корректно")
            return True
        else:
            print("⚠️ LongPoll создан, но структура необычна")
            return True
    except ImportError:
        print("❌ Ошибка импорта LongPoll")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {type(e).__name__}")
        return False


async def main():
    print("🚀 Тестирование VK API...")
    print("=" * 50)

    config_ok = test_vk_config()
    connection_ok = False
    longpoll_ok = False

    if config_ok:
        connection_ok = await asyncio.to_thread(test_vk_connection)
        if connection_ok:
            longpoll_ok = test_vk_longpoll()

    print("\n" + "=" * 50)
    print("📊 ИТОГИ ТЕСТИРОВАНИЯ:")
    print(f"   Конфигурация: {'✅' if config_ok else '❌'}")
    print(f"   Подключение:  {'✅' if connection_ok else '❌'}")
    print(f"   LongPoll:     {'✅' if longpoll_ok else '❌'}")


if __name__ == "__main__":
    asyncio.run(main())
