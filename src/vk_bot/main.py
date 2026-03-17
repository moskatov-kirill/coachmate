#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VK Bot для CoachMate — vkbottle 4.7.0 с отключенным SSL
"""
import os
import ssl

# ⚠️ ОТКЛЮЧАЕМ SSL — ДО ВСЕХ ИМПОРТОВ!
ssl._create_default_https_context = ssl._create_unverified_context
os.environ["PYTHONHTTPSVERIFY"] = "0"

import logging
from dotenv import load_dotenv
from vkbottle import Bot, API
from vkbottle.http import AiohttpClient
from vkbottle.bot import Message
from aiohttp import ClientSession, TCPConnector

load_dotenv()
logger = logging.getLogger(__name__)

VK_TOKEN = os.getenv("VK_GROUP_TOKEN")
if not VK_TOKEN:
    raise ValueError("❌ VK_GROUP_TOKEN не найден в .env")


# 🔥 Кастомный клиент с отключенным SSL
class NoSSLHttpClient(AiohttpClient):
    async def request(self, url, method, data=None, **kwargs):
        # Принудительно добавляем ssl=False к каждому запросу
        kwargs.setdefault("ssl", False)
        return await super().request(method, url, **kwargs)


# Создаём API с нашим кастомным клиентом
http_client = NoSSLHttpClient()
api = API(token=VK_TOKEN, http_client=http_client)
bot = Bot(api=api)

logger.info("🤖 Бот создан (кастомный HTTP-клиент, SSL=False)")


@bot.on.message()
async def handle_message(message: Message):
    logger.info(f"📨 Сообщение от {message.from_id}: {message.text}")
    await message.answer("Привет! Я CoachMate бот и я работаю! 🤖")
