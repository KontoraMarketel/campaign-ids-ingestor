from datetime import datetime, timedelta

import aiohttp

from utils import chunked

GET_ALL_ADS_URL = "https://advert-api.wildberries.ru/adv/v1/promotion/count"
GET_ADS_STATS_URL = "https://advert-api.wildberries.ru/adv/v2/fullstats"
GET_ADS_INFO_URL = "https://advert-api.wildberries.ru/adv/v1/promotion/adverts"


# <ts> это дата когда выполняется функция, найди от нее вчерашнюю дату и используй
async def fetch_data(api_token: str) -> (list, list):
    headers = {"Authorization": api_token}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(GET_ALL_ADS_URL) as response:
            data = await response.json()
            response.raise_for_status()
            return data['adverts']
