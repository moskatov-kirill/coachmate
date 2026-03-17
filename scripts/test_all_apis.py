#!/usr/bin/env python
"""
Полное тестирование всех API после миграции на VK
"""
import asyncio

# import os
from dotenv import load_dotenv

# Импортируем тесты
from test_apis import test_gigachat, test_google_fit
from test_db import test_database
from test_vk_api import test_vk_config, test_vk_connection

load_dotenv()


async def main():
    print("🚀 ПОЛНОЕ ТЕСТИРОВАНИЕ ПОСЛЕ МИГРАЦИИ НА VK")
    print("=" * 60)

    # 1. Тест VK
    print("\n📱 1. ТЕСТ VK API")
    vk_config = test_vk_config()
    vk_connection = False
    if vk_config:
        vk_connection = await asyncio.to_thread(test_vk_connection)

    # 2. Тест GigaChat
    print("\n🤖 2. ТЕСТ GIGACHAT API")
    gigachat_ok = test_gigachat()

    # 3. Тест Google Fit
    print("\n🏃 3. ТЕСТ GOOGLE FIT API")
    google_ok = test_google_fit()

    # 4. Тест базы данных
    print("\n🗄️ 4. ТЕСТ БАЗЫ ДАННЫХ")
    db_ok = test_database()

    # Итоги
    print("\n" + "=" * 60)
    print("📊 ИТОГИ ТЕСТИРОВАНИЯ:")
    print(f"   VK API:          {'✅' if vk_connection else '❌'}")
    print(f"   GigaChat:        {'✅' if gigachat_ok else '❌'}")
    print(f"   Google Fit:      {'✅' if google_ok else '❌'}")
    print(f"   База данных:     {'✅' if db_ok else '❌'}")

    all_ok = vk_connection and gigachat_ok and google_ok and db_ok
    if all_ok:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Миграция на VK успешна!")
    else:
        print("\n⚠️ Некоторые тесты не пройдены. Проверьте ошибки выше.")


if __name__ == "__main__":
    asyncio.run(main())
