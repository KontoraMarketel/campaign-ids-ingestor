from datetime import datetime, timedelta

import aiohttp

from utils import chunked

GET_ALL_ADS_URL = "https://advert-api.wildberries.ru/adv/v1/promotion/count"
GET_ADS_STATS_URL = "https://advert-api.wildberries.ru/adv/v2/fullstats"
GET_ADS_INFO_URL = "https://advert-api.wildberries.ru/adv/v1/promotion/adverts"


# <ts> это дата когда выполняется функция, найди от нее вчерашнюю дату и используй
async def fetch_data(api_token: str) -> (list, list):
    headers = {"Authorization": api_token}
    #
    # dt_ts = datetime.fromisoformat(ts)
    # yesterday = (dt_ts - timedelta(days=1)).strftime("%Y-%m-%d")

    async with aiohttp.ClientSession(headers=headers) as session:
        campaign_ids = await _fetch_all_campaigns(session)

        return campaign_ids


async def _fetch_all_campaigns_info(session: aiohttp.ClientSession, campaign_ids: list) -> list:
    result = []
    for batch in chunked(campaign_ids, 50):
        async with session.post(GET_ADS_INFO_URL, json=batch) as response:
            data = await response.json()
            response.raise_for_status()
            result.extend(data)
    return result


async def _fetch_ad_stats(session: aiohttp.ClientSession, campaign_ids: list, yesterday) -> dict:
    result = []
    body = [{"id": cid, "dates": [yesterday]} for cid in campaign_ids]
    for batch in chunked(body, 100):
        async with session.post(GET_ADS_STATS_URL, body=batch) as response:
            data = await response.json()
            response.raise_for_status()
            result.extend(data)
    return result


async def _fetch_all_campaigns(session: aiohttp.ClientSession) -> str:
    async with session.get(GET_ALL_ADS_URL) as response:
        data = await response.json()
        response.raise_for_status()
        return data
