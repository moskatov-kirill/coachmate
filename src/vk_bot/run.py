#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

current_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(current_dir))

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", force=True
)
logger = logging.getLogger(__name__)

load_dotenv()

if not os.getenv("VK_GROUP_TOKEN"):
    logger.error("❌ VK_GROUP_TOKEN не найден")
    sys.exit(1)

from main import bot


def main():
    logger.info("🚀 Запуск VK бота...")
    try:
        bot.run_forever()
    except KeyboardInterrupt:
        logger.info("⏹️ Остановка пользователем")
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}", exc_info=True)


if __name__ == "__main__":
    main()
