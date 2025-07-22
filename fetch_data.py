import asyncio
import logging

import aiohttp

GET_ALL_ADS_URL = "https://advert-api.wildberries.ru/adv/v1/promotion/count"


# <ts> это дата когда выполняется функция, найди от нее вчерашнюю дату и используй
async def fetch_data(api_token: str) -> (list, list):
    headers = {"Authorization": api_token}
    async with aiohttp.ClientSession(headers=headers) as session:
        data = await fetch_page_with_retry(session, GET_ALL_ADS_URL)
        return data['adverts']


async def fetch_page_with_retry(session, url):
    while True:
        async with session.get(url) as response:
            if response.status == 429:
                retry_after = int(response.headers.get('X-Ratelimit-Retry', 10))
                logging.warning(f"Rate limited (429). Retrying after {retry_after} seconds...")
                await asyncio.sleep(retry_after)
                continue

            response.raise_for_status()
            return await response.json()
