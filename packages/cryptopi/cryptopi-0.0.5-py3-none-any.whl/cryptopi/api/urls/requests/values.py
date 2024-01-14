"""
values.py Contains Enums and models for API request data.
"""
from enum import Enum
from typing import Final


class ListingStatus(str, Enum):
    """
    The listing status for a cryptocurrency.
    """

    ACTIVE: Final[str] = "active"
    INACTIVE: Final[str] = "inactive"
    UNLISTED: Final[str] = "unlisted"


class MapSortValue(str, Enum):
    """
    The supported sort values for the `/cryptocurrency/map` endpoint.
    """

    ID: Final[str] = "id"
    CMC_RANK: Final[str] = "cmc_rank"


class MapAux(str, Enum):
    """
    Supplemental data points to return.
    """

    PLATFORM: Final[str] = "platform"
    FIRST_HISTORICAL_DATA: Final[str] = "first_historical_data"
    LAST_HISTORICAL_DATA: Final[str] = "last_historical_data"
    IS_ACTIVE: Final[str] = "is_active"
    STATUS: Final[str] = "status"


class ListingSortValue(str, Enum):
    """
    The supported sort values for the `/cryptocurrency/listings` endpoints.
    """

    MARKET_CAP: Final[str] = "market_cap"
    NAME: Final[str] = "name"
    SYMBOL: Final[str] = "symbol"
    DATE_ADDED: Final[str] = "date_added"
    MARKET_CAP_STRICT: Final[str] = "market_cap_strict"
    PRICE: Final[str] = "price"
    CIRCULATING_SUPPLY: Final[str] = "circulating_supply"
    TOTAL_SUPPLY: Final[str] = "total_supply"
    MAX_SUPPLY: Final[str] = "max_supply"
    NUM_MARKET_PAIRS: Final[str] = "num_market_pairs"
    VOLUME_24H: Final[str] = "volume_24h"
    PERCENT_CHANGE_1H: Final[str] = "percent_change_1h"
    PERCENT_CHANGE_24H: Final[str] = "percent_change_24h"
    PERCENT_CHANGE_7D: Final[str] = "percent_change_7d"
    MARKET_CAP_BY_TOTAL_SUPPLY_STRICT: Final[str] = "market_cap_by_total_supply_strict"
    VOLUME_7D: Final[str] = "volume_7d"
    VOLUME_30D: Final[str] = "volume_30d"


class ListingSortDirection(str, Enum):
    """
    The sort direction for the `/cryptocurrency/listings` endpoints.
    """

    ASCENDING: Final[str] = "asc"
    DESCENDING: Final[str] = "desc"


class ListingTag(str, Enum):
    """
    The tag of cryptocurrency to include.
    """

    ALL: Final[str] = "all"
    DEFI: Final[str] = "defi"
    FILE_SHARING: Final[str] = "filesharing"


class CryptoCurrencyType(str, Enum):
    """
    The type of cryptocurrency.
    """

    ALL: Final[str] = "all"
    COINS: Final[str] = "coins"
    TOKENS: Final[str] = "tokens"


class ListingAux(str, Enum):
    """
    Supplemental data points to return.
    """

    NUM_MARKET_PAIRS: Final[str] = "num_market_pairs"
    CMC_RANK: Final[str] = "cmc_rank"
    DATE_ADDED: Final[str] = "date_added"
    TAGS: Final[str] = "tags"
    PLATFORM: Final[str] = "platform"
    MAX_SUPPLY: Final[str] = "max_supply"
    CIRCULATING_SUPPLY: Final[str] = "circulating_supply"
    TOTAL_SUPPLY: Final[str] = "total_supply"
    MARKET_CAP_BY_TOTAL_SUPPLY: Final[str] = "market_cap_by_total_supply"
    VOLUME_24H_REPORTED: Final[str] = "volume_24h_reported"
    VOLUME_7D: Final[str] = "volume_7d"
    VOLUME_7D_REPORTED: Final[str] = "volume_7d_reported"
    VOLUME_30D: Final[str] = "volume_30d"
    VOLUME_30D_REPORTED: Final[str] = "volume_30d_reported"
    IS_MARKET_CAP_INCLUDED_IN_CALCULATIONS: Final[
        str
    ] = "is_market_cap_included_in_calc"


class QuoteAux(str, Enum):
    """
    Supplemental data points to return.
    """

    NUM_MARKET_PAIRS: Final[str] = "num_market_pairs"
    CMC_RANK: Final[str] = "cmc_rank"
    DATE_ADDED: Final[str] = "date_added"
    TAGS: Final[str] = "tags"
    PLATFORM: Final[str] = "platform"
    MAX_SUPPLY: Final[str] = "max_supply"
    CIRCULATING_SUPPLY: Final[str] = "circulating_supply"
    TOTAL_SUPPLY: Final[str] = "total_supply"
    MARKET_CAP_BY_TOTAL_SUPPLY: Final[str] = "market_cap_by_total_supply"
    VOLUME_24H_REPORTED: Final[str] = "volume_24h_reported"
    VOLUME_7D: Final[str] = "volume_7d"
    VOLUME_7D_REPORTED: Final[str] = "volume_7d_reported"
    VOLUME_30D: Final[str] = "volume_30d"
    VOLUME_30D_REPORTED: Final[str] = "volume_30d_reported"
    IS_ACTIVE: Final[str] = "is_active"
    IS_FIAT: Final[str] = "is_fiat"
