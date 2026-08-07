import aiohttp

http_session: aiohttp.ClientSession | None = None

async def init_session():
    global http_session
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    http_session = aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=10),
        headers=headers
    )

async def close_session():
    global http_session
    if http_session:
        await http_session.close()
        http_session = None