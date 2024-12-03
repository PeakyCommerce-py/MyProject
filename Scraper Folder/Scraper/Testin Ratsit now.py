import aiohttp
import asyncio

async def fetch(url, headers=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            print("Status:", response.status)
            if response.status == 200:
                return await response.text()
            else:
                print("Error:", response.status)
                return None

async def main():
    url = "https://www.ratsit.se/sok/person?vem=Arjeplog&m=0&k=0&r=0&er=0&b=0&eb=0&amin=16&amax=120&fon=1&page=2"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive"
    }
    content = await fetch(url, headers)
    if content:
        print("Content received:")
        print(content[:500])  # Print the first 500 characters for inspection

# Kör main funktionen
asyncio.run(main())
