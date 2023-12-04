from typing import Optional

import aiohttp

from enums import SortOrder

from .base import ApiBase, ProductData


class AmazonApi(ApiBase):
    __host: str
    __api_key: str
    __session: aiohttp.ClientSession

    def __init__(self, host: str, api_key: str) -> None:
        self.__host = host
        self.__api_key = api_key
        self.__session = aiohttp.ClientSession()

    async def get_prices(
        self,
        query: str,
        page: Optional[int] = 1,
        sort_by: SortOrder = SortOrder.RELEVANCE,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
    ) -> list[ProductData]:
        url = f"https://{self.__host}/search"
        params = {
            "query": query,
            "page": page,
            "sort_by": sort_by,
        }

        headers = {"X-RapidAPI-Host": self.__host, "X-RapidAPI-Key": self.__api_key}

        if min_price is not None:
            params["min_price"] = min_price

        if max_price is not None:
            params["max_price"] = max_price

        async with self.__session.get(url, params=params, headers=headers) as resp:
            resp_json = await resp.json()
            result: list[ProductData] = resp_json["data"]["products"]
            return result

    async def destroy(self):
        await self.__session.close()
