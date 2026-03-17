#!/usr/bin/env python
"""
Тестирование подключения к SQLite и проверка наличия таблиц
"""
import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def test_database():
    print("🗄️ Тестирование SQLite...")

    db_path = os.getenv("SQLITE_PATH", "data/sqlite/coachmate.db")
    print(f"📁 Путь к БД: {db_path}")

    if not os.path.exists(db_path):
        print(f"❌ Файл базы данных не найден: {db_path}")
        print("💡 Запусти сначала: python scripts/init_db.py")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        all_tables = cursor.fetchall()
        existing_tables = [t[0] for t in all_tables]

        print(
            f"\n📊 Все таблицы в БД: {', '.join(existing_tables) if existing_tables else 'нет таблиц'}"
        )

        required_tables = [
            "users",
            "health_metrics",
            "google_fit_activities",
            "usage_logs",
            "reminders",
        ]

        print("\n🔍 Проверка необходимых таблиц:")
        all_exist = True
        for table in required_tables:
            if table in existing_tables:
                print(f"  ✅ {table} - существует")
            else:
                print(f"  ❌ {table} - отсутствует")
                all_exist = False

        if all_exist:
            print("\n📈 Статистика по таблицам:")
            for table in required_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  • {table}: {count} записей")

        conn.close()

        if all_exist:
            print("\n✅ Все необходимые таблицы созданы корректно")
            return True
        else:
            print("\n⚠️ Некоторые таблицы отсутствуют. Запусти: python scripts/init_db.py")
            return False
    except sqlite3.Error as e:
        print(f"❌ Ошибка SQLite: {e}")
        return False


if __name__ == "__main__":
    test_database()
