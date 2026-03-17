# scripts/test_apis.py
#!/usr/bin/env python
"""
Тестирование доступности всех API перед началом разработки.
"""
import os
import asyncio
from dotenv import load_dotenv
from gigachat import GigaChat
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

load_dotenv()


def test_telegram():
    print("\n📱 Тестирование Telegram API...")
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN не найден в .env")
        return False

    url = f"https://api.telegram.org/bot{token}/getMe"
    response = requests.get(url)

    if response.status_code == 200 and response.json()["ok"]:
        bot_name = response.json()["result"]["username"]
        print(f"✅ Telegram бот @{bot_name} доступен")
        return True
    print(f"❌ Ошибка Telegram API: {response.text}")
    return False


def test_gigachat():
    print("\n🤖 Тестирование GigaChat API...")
    credentials = os.getenv("GIGACHAT_CREDENTIALS")
    if not credentials:
        print("❌ GIGACHAT_CREDENTIALS не найдены в .env")
        return False

    try:
        with GigaChat(credentials=credentials, verify_ssl_certs=False) as giga:
            token_info = giga.get_token()
            print(f"✅ Токен получен, expires at: {getattr(token_info, 'expires_at', 'unknown')}")

            models_response = giga.get_models()
            if hasattr(models_response, "data"):
                models_list = models_response.data
                print(f"✅ GigaChat доступен, найдено моделей: {len(models_list)}")
                for model in models_list:
                    print(f"   - {getattr(model, 'id', 'unknown')}")
            else:
                print(f"✅ GigaChat доступен")

            try:
                chat_response = giga.chat("Привет! Ответь одним словом.")
                print(f"✅ Тестовый запрос выполнен")
            except Exception as chat_error:
                print(f"⚠️ Тестовый запрос не удался: {chat_error}")

            return True
    except Exception as e:
        print(f"❌ Ошибка GigaChat: {type(e).__name__}: {e}")
        return False


def test_google_fit():
    print("\n🏃 Тестирование Google Fit...")
    client_secrets_file = os.getenv("GOOGLE_CLIENT_SECRETS_FILE")
    token_file = os.getenv("GOOGLE_FIT_TOKEN_FILE")

    if not client_secrets_file or not os.path.exists(client_secrets_file):
        print(f"❌ Файл client_secrets не найден: {client_secrets_file}")
        return False

    SCOPES = [
        "https://www.googleapis.com/auth/fitness.activity.read",
        "https://www.googleapis.com/auth/fitness.body.read",
    ]

    creds = None
    if os.path.exists(token_file):
        import json

        with open(token_file, "r") as token:
            creds_data = json.load(token)
            creds = Credentials.from_authorized_user_info(creds_data, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print("✅ Токен Google Fit обновлен")
        else:
            print("🔄 Запускаем OAuth 2.0 flow для Google Fit...")
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)
            os.makedirs(os.path.dirname(token_file), exist_ok=True)
            with open(token_file, "w") as token:
                token.write(creds.to_json())
            print(f"✅ Токен сохранен")

    try:
        service = build("fitness", "v1", credentials=creds)
        datasets = service.users().dataSources().list(userId="me").execute()
        print("✅ Google Fit API доступен")
        return True
    except Exception as e:
        print(f"❌ Ошибка Google Fit API: {e}")
        return False


async def main():
    print("🚀 Начинаем тестирование API...")
    print("=" * 50)

    results = [test_telegram(), test_gigachat(), test_google_fit()]

    print("\n" + "=" * 50)
    success_count = sum(1 for r in results if r)
    print(f"📊 Результаты: {success_count}/{len(results)} тестов пройдено")


if __name__ == "__main__":
    asyncio.run(main())
