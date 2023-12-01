import json
import os
from typing import Optional

from enums import SortOrder

from .base import ApiBase, ProductData


class MockApi(ApiBase):
    async def get_prices(
        self,
        query: str,
        page: Optional[int] = 1,
        sort_by: Optional[str] = SortOrder.RELEVANCE,
        min_price: float | None = None,
        max_price: Optional[float] = None,
    ) -> list[ProductData]:
        with open(os.path.join("mock_data", "test_response.json")) as test_responses:
            mock_data: list[ProductData] = json.load(test_responses)

        return mock_data

    async def get_low_prices(self, query: str) -> list[ProductData]:
        with open(os.path.join("mock_data", "test_response_2.json")) as test_responses:
            mock_data: list[ProductData] = json.load(test_responses)

        return mock_data

    async def get_high_prices(self, query: str) -> list[ProductData]:
        with open(os.path.join("mock_data", "test_response.json")) as test_response:
            mock_data: list[ProductData] = json.load(test_response)

        return mock_data

    async def get_custom_prices(
        self,
        query: str,
        min_price: float,
        max_price: float,
    ) -> list[ProductData]:
        with open(os.path.join("mock_data", "test_response.json")) as test_responses:
            mock_data: list[ProductData] = json.load(test_responses)

        return mock_data

    async def destroy(self):
        ...
