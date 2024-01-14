"""
paths.py This file contains the CryptoCurrencyUrl paths for the API.
"""
from enum import Enum
from typing import Final
from urllib.parse import urljoin


class BaseUrl(str, Enum):
    """
    The base CryptoCurrencyUrl.
    """

    SANDBOX: Final[str] = "https://sandbox-api.coinmarketcap.com/"
    PRODUCTION: Final[str] = "https://pro-api.coinmarketcap.com/"


class ApiVersion(str, Enum):
    """
    The API versions.
    """

    V1: Final[str] = "v1/"


class PathPart(str, Enum):
    """
    Part of a CryptoCurrencyUrl path.
    """

    CRYPTOCURRENCY = "cryptocurrency/"
    LISTINGS = "listings/"
    QUOTES = "quotes/"
    LATEST = "latest"
    HISTORICAL = "historical"
    MAP = "map"
    INFO = "info/"
    MARKET_PAIRS = "market-pairs/"
    OHLCV = "ohlcv/"
    PRICE_PERFORMANCE_STATS = "price-performance-stats/"
    CATEGORIES = "categories/"
    CATEGORY = "category/"
    AIRDROPS = "airdrops/"
    AIRDROP = "airdrop/"
    TRENDING = "trending/"
    MOST_VISITED = "most-visited/"
    GAINERS_LOSERS = "gainers-losers/"


# noinspection PyTypeChecker
class CryptoCurrencyListings(str, Enum):
    """
    The paths for the `/cryptocurrency/listings` endpoint.
    """

    LATEST: Final[str] = urljoin(
        PathPart.CRYPTOCURRENCY, urljoin(PathPart.LISTINGS, PathPart.LATEST)
    )
    HISTORICAL: Final[str] = urljoin(
        PathPart.CRYPTOCURRENCY, PathPart.LISTINGS, PathPart.HISTORICAL
    )


# noinspection PyTypeChecker
class CryptoCurrencyQuotes(str, Enum):
    """
    The paths for the `/cryptocurrency/quotes` endpoint.
    """

    LATEST: Final[str] = urljoin(
        PathPart.CRYPTOCURRENCY, urljoin(PathPart.QUOTES, PathPart.LATEST)
    )
    HISTORICAL: Final[str] = urljoin(
        PathPart.CRYPTOCURRENCY, urljoin(PathPart.QUOTES, PathPart.HISTORICAL)
    )


class CryptoCurrencyMarketPairs(str, Enum):
    """
    The paths for the `/cryptocurrency/market-pairs` endpoint.
    """

    LATEST: Final[str] = urljoin(
        PathPart.CRYPTOCURRENCY, urljoin(PathPart.MARKET_PAIRS, PathPart.LATEST)
    )


class CryptoCurrencyOhlcv(str, Enum):
    """
    The paths for the `/cryptocurrency/ohlcv` endpoint.
    """

    LATEST: Final[str] = urljoin(
        PathPart.CRYPTOCURRENCY, urljoin(PathPart.OHLCV, PathPart.LATEST)
    )
    HISTORICAL: Final[str] = urljoin(
        PathPart.CRYPTOCURRENCY, urljoin(PathPart.OHLCV, PathPart.HISTORICAL)
    )


class CryptoCurrencyPricePerformanceStats(str, Enum):
    """
    The paths for the `/cryptocurrency/price-performance-stats` endpoint.
    """

    LATEST: Final[str] = urljoin(
        PathPart.CRYPTOCURRENCY,
        urljoin(PathPart.PRICE_PERFORMANCE_STATS, PathPart.LATEST),
    )


class CryptoCurrencyTrending(str, Enum):
    """
    The paths for the `/cryptocurrency/trending` endpoint.
    """

    LATEST: Final[str] = urljoin(
        PathPart.CRYPTOCURRENCY, urljoin(PathPart.TRENDING, PathPart.LATEST)
    )
    MOST_VISITED: Final[str] = urljoin(
        PathPart.CRYPTOCURRENCY, urljoin(PathPart.TRENDING, PathPart.MOST_VISITED)
    )
    GAINERS_LOSERS: Final[str] = urljoin(
        PathPart.CRYPTOCURRENCY, urljoin(PathPart.TRENDING, PathPart.GAINERS_LOSERS)
    )


class CryptoCurrencyPaths(str, Enum):
    """
    The paths for the `/cryptocurrency` endpoint.
    """

    MAP: Final[str] = urljoin(PathPart.CRYPTOCURRENCY, PathPart.MAP)
    INFO: Final[str] = urljoin(PathPart.CRYPTOCURRENCY, PathPart.INFO)
    LISTINGS_LATEST: Final[str] = CryptoCurrencyListings.LATEST.value
    LISTINGS_HISTORICAL: Final[str] = CryptoCurrencyListings.HISTORICAL
    QUOTES_LATEST: Final[str] = CryptoCurrencyQuotes.LATEST.value
    QUOTES_HISTORICAL: Final[str] = CryptoCurrencyQuotes.HISTORICAL
    MARKET_PAIRS_LATEST: Final[str] = CryptoCurrencyMarketPairs.LATEST
    OHLCV_LATEST: Final[str] = CryptoCurrencyOhlcv.LATEST
    OHLCV_HISTORICAL: Final[str] = CryptoCurrencyOhlcv.HISTORICAL
    PRICE_PERFORMANCE_STATS_LATEST: Final[
        str
    ] = CryptoCurrencyPricePerformanceStats.LATEST

    CATEGORIES: Final[str] = urljoin(PathPart.CRYPTOCURRENCY, PathPart.CATEGORIES)
    CATEGORY: Final[str] = urljoin(PathPart.CRYPTOCURRENCY, PathPart.CATEGORY)
    AIRDROPS: Final[str] = urljoin(PathPart.CRYPTOCURRENCY, PathPart.AIRDROPS)
    AIRDROP: Final[str] = urljoin(PathPart.CRYPTOCURRENCY, PathPart.AIRDROP)

    TRENDING_LATEST: Final[str] = CryptoCurrencyTrending.LATEST
    TRENDING_MOST_VISITED: Final[str] = CryptoCurrencyTrending.MOST_VISITED
    TRENDING_GAINERS_LOSERS: Final[str] = CryptoCurrencyTrending.GAINERS_LOSERS
