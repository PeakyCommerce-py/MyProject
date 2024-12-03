import aiohttp
import asyncio
import pandas as pd
from urllib.parse import urlencode, urlparse, parse_qs


def convert_to_api_url(web_url):
    base_api_url = "https://api.kontorsgiganten.se/v1/products/search.json"
    url_parts = urlparse(web_url)
    query_params = parse_qs(url_parts.query)
    if 'q' in query_params:
        query = query_params['q'][0]
        api_query = {'q': query, 'offset': 0, 'limit': 24, 'server': 'search01'}
        api_url = f"{base_api_url}?{urlencode(api_query)}"
        return api_url
    return None


async def get_total_from_api(session, api_url):
    async with session.get(api_url) as response:
        if response.status == 200:
            data = await response.json()
            if 'total' in data:
                return data['total']
    return None


async def process_link(session, web_url):
    api_url = convert_to_api_url(web_url)
    if api_url:
        total = await get_total_from_api(session, api_url)
        if total is not None:
            return web_url, total
    return web_url, None


async def process_links(file_path, max_links=10000):
    async with aiohttp.ClientSession() as session:
        with open(file_path, 'r') as file:
            links = [link.strip() for link in file.readlines()]

        tasks = []
        count = 0
        for link in links:
            if count >= max_links:
                break
            tasks.append(process_link(session, link))
            count += 1

        results = await asyncio.gather(*tasks)
        return results


def save_to_excel(data, file_name='output.xlsx'):
    df = pd.DataFrame(data, columns=['URL', 'Total'])
    df.to_excel(file_name, index=False)
    print(f"Data saved to {file_name}")


if __name__ == "__main__":
    file_path = 'execution.txt'
    results = asyncio.run(process_links(file_path, max_links=10000))
    save_to_excel(results)
