#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для инициализации базы данных SQLite.
Запускать один раз при первом развертывании.
"""
import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Путь к базе данных
DB_PATH = os.getenv("SQLITE_PATH", "data/sqlite/coachmate.db")


def init_database():
    """Создание всех таблиц в базе данных."""
    print(f"🗄️ Инициализация базы данных: {DB_PATH}")

    # Создаем директорию, если её нет
    db_dir = os.path.dirname(DB_PATH)
    if db_dir:
        Path(db_dir).mkdir(parents=True, exist_ok=True)
        print(f"📁 Директория создана/проверена: {db_dir}")

    # Проверяем права на запись
    test_file = os.path.join(db_dir, "write_test.tmp")
    try:
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        print("✅ Права на запись есть")
    except Exception as e:
        print(f"❌ Нет прав на запись в {db_dir}: {e}")
        return False

    try:
        # Подключаемся к БД
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Таблица пользователей
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                telegram_username TEXT,
                first_name TEXT,
                last_name TEXT,
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                preferences TEXT
            )
        """
        )

        # Таблица метрик здоровья
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS health_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date DATE DEFAULT CURRENT_DATE,
                weight REAL,
                systolic_pressure INTEGER,
                diastolic_pressure INTEGER,
                pulse INTEGER,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """
        )

        # Таблица для Google Fit активностей
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS google_fit_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                activity_date DATE,
                steps INTEGER,
                calories INTEGER,
                active_minutes INTEGER,
                heart_rate_avg INTEGER,
                heart_rate_max INTEGER,
                distance_km REAL,
                raw_data TEXT,
                synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """
        )

        # Таблица для логов использования
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usage_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                command TEXT,
                parameters TEXT,
                response_time_ms INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """
        )

        # Таблица для напоминаний
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                reminder_type TEXT,
                reminder_time TIME,
                is_active BOOLEAN DEFAULT 1,
                last_triggered DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """
        )

        conn.commit()

        # Проверяем, что таблицы создались
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"\n📊 Созданные таблицы: {', '.join(t[0] for t in tables)}")

        conn.close()
        print("\n✅ База данных успешно инициализирована")
        return True

    except sqlite3.Error as e:
        print(f"❌ Ошибка SQLite: {e}")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return False


def test_connection():
    """Проверка подключения к БД."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT sqlite_version()")
        version = cursor.fetchone()[0]
        conn.close()
        print(f"✅ Подключение к SQLite {version} успешно")
        return True
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Начинаем инициализацию базы данных...")
    print("=" * 50)

    if test_connection():
        init_database()
    else:
        print("\n❌ Ошибка инициализации базы данных")
