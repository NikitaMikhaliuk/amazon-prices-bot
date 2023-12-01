from enum import Enum, StrEnum


class PyEnv(StrEnum):
    PRODUCTION = "PRODUCTION"
    DEV = "DEV"


class Commands(StrEnum):
    PREFIX = "/"
    START = "start"
    HELP = "help"
    LOW = "low"
    HIGH = "high"
    CUSTOM = "custom"


class SortOrder(StrEnum):
    RELEVANCE = "RELEVANCE"
    LOWEST_PRICE = "LOWEST_PRICE"
    HIGHEST_PRICE = "HIGHEST_PRICE"
    REVIEWS = "REVIEWS"
    NEWEST = "NEWEST"
    BEST_SELLERS = "BEST_SELLERS"


class ViewLimit(Enum):
    MIN = 1
    MAX = 5
