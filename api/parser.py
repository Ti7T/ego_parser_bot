import aiohttp
import asyncio
from config import BASE_URL, APIEndpoints
import base64
from api import client

async def get_player_json(nick: str) -> dict | None:
    return await parse_url(APIEndpoints.PROFILE_BY_NICK.format(nick=nick))

async def get_player_playtime_json(nick: str) -> dict | None:
    return await parse_url(APIEndpoints.PLAYTIME_BY_NICK.format(nick=nick))

async def parse_url(endpoint: str) -> dict | None:
    try:
        session = client.http_session
        async with session.get(f"{BASE_URL}{endpoint}") as response:
            response.raise_for_status()
            return await response.json()
    except aiohttp.ClientResponseError as e:
        # Ошибки HTTP (4xx, 5xx)
        print(f"HTTP error: {e.status} - {e.message}")
        return None
    except aiohttp.ClientConnectionError as e:
        # Ошибки соединения (таймаут, DNS, отказ сервера)
        print(f"Connection error: {e}")
        return None
    except asyncio.TimeoutError:
        print("Request timed out")
        return None
    except aiohttp.ContentTypeError:
        # Сервер вернул не JSON (или заголовок Content-Type не JSON)
        print("Сервер вернул не JSON.")
        return None
    except Exception as e:
        # Любые другие ошибки
        print(f"Unexpected error: {e}")
        return None

async def url_to_base64_async(url: str) -> str:
    session = client.http_session
    async with session.get(url) as response:
        response.raise_for_status()
        content_type = response.headers.get('content-type', 'image/png')
        data = await response.read()
        b64 = base64.b64encode(data).decode()
        return f"data:{content_type};base64,{b64}"

async def main():
    try:
        url = "https://eternal-gores.com/api/profiles/by-nick/ZнdyyR"
        # url = "https://eternal-gores.com/api/profiles/by-nick/axech"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10), headers=headers)
        result = await get_player_json(url, session)
        if result:
            print(result)
    finally:
        await session.close()

if __name__ == "__main__":
    asyncio.run(main())
    