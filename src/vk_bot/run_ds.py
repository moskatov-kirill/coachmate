#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Отдельный файл для запуска VK бота с правильным event loop
"""
import asyncio
import logging
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Добавляем корневую папку проекта в путь Python
# Это решит проблему с импортом src
current_dir = Path(__file__).resolve().parent
project_root = (
    current_dir.parent.parent
)  # поднимаемся на 2 уровня вверх: src/vk_bot -> src -> корень
sys.path.insert(0, str(project_root))

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Загружаем переменные окружения
load_dotenv(os.path.join(project_root, ".env"))

# Теперь импорт должен работать
from main import bot


async def main():
    """Асинхронная функция запуска бота"""
    logger.info("🚀 Запуск VK бота из run.py...")

    try:
        # Запускаем бота
        await bot.run_polling()
    except Exception as e:
        logger.error(f"❌ Ошибка при работе бота: {e}")
        import traceback

        logger.error(traceback.format_exc())
    finally:
        logger.info("👋 Бот остановлен")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹️ Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
