from abc import ABC, abstractmethod
from typing import Optional, TypedDict

from enums import SortOrder


class ProductData(TypedDict):
    product_title: str
    product_price: Optional[str]
    product_url: str
    product_photo: str


class ApiBase(ABC):
    @abstractmethod
    def get_prices(
        self,
        query: str,
        page: Optional[int] = 1,
        sort_by: Optional[str] = SortOrder.RELEVANCE,
        min_price: float | None = None,
        max_price: Optional[float] = None,
    ) -> list[ProductData]:
        ...

    @abstractmethod
    def destroy(self):
        ...
