"""
Тестирование Telegram API через прокси (для РФ).
"""

import os

import requests
from dotenv import load_dotenv

load_dotenv()


def test_telegram_with_proxy():
    """Проверка Telegram Bot API через прокси."""
    print("\n📱 Тестирование Telegram API...")

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN не найден в .env")
        return False

    # Настройки прокси (если используешь)
    proxies = {"http": os.getenv("HTTP_PROXY", ""), "https": os.getenv("HTTPS_PROXY", "")}

    url = f"https://api.telegram.org/bot{token}/getMe"

    try:
        if proxies["http"] or proxies["https"]:
            print(f"🔄 Использую прокси: {proxies}")
            response = requests.get(url, proxies=proxies, timeout=10)
        else:
            print("🔄 Без прокси")
            response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data["ok"]:
                bot_name = data["result"]["username"]
                print(f"✅ Telegram бот @{bot_name} доступен")
                return True
        print(f"❌ Ошибка Telegram API: {response.text}")
        return False

    except requests.exceptions.ProxyError:
        print("❌ Ошибка прокси. Проверь настройки.")
        return False
    except requests.exceptions.ConnectTimeout:
        print("❌ Таймаут подключения. Возможно, нужен прокси.")
        return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


if __name__ == "__main__":
    test_telegram_with_proxy()
