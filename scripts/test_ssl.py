import ssl

print(f"SSL Context: {ssl.get_default_verify_paths()}")

import aiohttp

print(f"aiohttp version: {aiohttp.__version__}")

import asyncio


async def test():
    connector = aiohttp.TCPConnector(ssl=False)
    session = aiohttp.ClientSession(connector=connector)
    try:
        async with session.get("https://api.vk.ru") as resp:
            print(f"✅ VK API доступ: {resp.status}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await session.close()


asyncio.run(test())
