"""
models.py Contains models for API request data.
"""
from typing import List
from typing import Optional

from cryptopi.api.urls.data import Symbol
from cryptopi.api.urls.requests.values import CryptoCurrencyType
from cryptopi.api.urls.requests.values import ListingAux
from cryptopi.api.urls.requests.values import ListingSortDirection
from cryptopi.api.urls.requests.values import ListingSortValue
from cryptopi.api.urls.requests.values import ListingStatus
from cryptopi.api.urls.requests.values import ListingTag
from cryptopi.api.urls.requests.values import MapAux
from cryptopi.api.urls.requests.values import MapSortValue
from cryptopi.api.urls.requests.values import QuoteAux
from pydantic import BaseModel
from pydantic import Field
from pydantic import field_serializer


class CryptoCurrenciesMapParams(BaseModel):
    listing_status: Optional[List[ListingStatus]] = Field(
        default=[ListingStatus.ACTIVE],
        description="The listing status for the cryptocurrency.",
    )
    start: Optional[int] = Field(
        default=1,
        description="Optionally offset the start (1-based index) of the paginated list of items to return.",
    )
    limit: Optional[int] = Field(
        100,
        description="Optionally specify the number of results to return. Use this parameter and the 'start' parameter to determine your own pagination size.",
    )
    sort: Optional[MapSortValue] = Field(
        default=MapSortValue.ID, description="The sort order of the returned data."
    )
    symbol: Optional[List[Symbol]] = Field(
        None,
        description="Optionally pass a comma-separated list of cryptocurrency symbols to return CoinMarketCap IDs for. If this option is passed, other options will be ignored.",
    )
    aux: Optional[List[MapAux]] = Field(
        default=[
            MapAux.PLATFORM,
            MapAux.FIRST_HISTORICAL_DATA,
            MapAux.LAST_HISTORICAL_DATA,
            MapAux.IS_ACTIVE,
            MapAux.STATUS,
        ],
        description="Optionally specify a comma-separated list of supplemental data fields to return. Pass 'platform,max_supply,circulating_supply,total_supply,cmc_rank,date_added,tags,num_market_pairs,notice,status' to include all auxiliary fields.",
    )

    # noinspection PyNestedDecorators
    @field_serializer("listing_status", "symbol", "aux")
    @classmethod
    def serialize(cls, value: List) -> Optional[str]:
        """
        Serialize the value.
        :param value: The value.
        :return:
        """

        return ",".join(value)


class CryptoCurrenciesListingParams(BaseModel):
    start: Optional[int] = Field(
        default=1,
        description="Optionally offset the start (1-based index) of the paginated list of items to return.",
    )
    limit: Optional[int] = Field(
        100,
        description="Optionally specify the number of results to return. Use this parameter and the 'start' parameter to determine your own pagination size.",
    )
    price_min: Optional[int] = Field(
        None,
        description="Optionally specify a threshold of minimum USD price to filter results by.",
    )
    price_max: Optional[int] = Field(
        None,
        description="Optionally specify a threshold of maximum USD price to filter results by.",
    )
    market_cap_min: Optional[int] = Field(
        None,
        description="Optionally specify a threshold of minimum USD market capitalization to filter results by.",
    )
    market_cap_max: Optional[int] = Field(
        None,
        description="Optionally specify a threshold of maximum USD market capitalization to filter results by.",
    )
    volume_24h_min: Optional[int] = Field(
        None,
        description="Optionally specify a threshold of minimum USD 24-hour volume to filter results by.",
    )
    volume_24h_max: Optional[int] = Field(
        None,
        description="Optionally specify a threshold of maximum USD 24-hour volume to filter results by.",
    )
    circulating_supply_min: Optional[int] = Field(
        None,
        description="Optionally specify a threshold of minimum circulating supply to filter results by.",
    )
    circulating_supply_max: Optional[int] = Field(
        None,
        description="Optionally specify a threshold of maximum circulating supply to filter results by.",
    )
    percent_change_24h_min: Optional[int] = Field(
        None,
        description="Optionally specify a threshold of minimum 24-hour percent change to filter results by.",
    )
    percent_change_24h_max: Optional[int] = Field(
        None,
        description="Optionally specify a threshold of maximum 24-hour percent change to filter results by.",
    )
    convert: Optional[List[Symbol]] = Field(
        None,
        description="Optionally calculate market quotes in up to 120 currencies at once by passing a comma-separated list of cryptocurrency or fiat currency symbols. Each additional convert option beyond the first requires an additional call credit. A list of supported fiat options can be found here.",
    )
    sort: Optional[ListingSortValue] = Field(
        ListingSortValue.MARKET_CAP, description="The sort order of the returned data."
    )
    sort_dir: Optional[ListingSortDirection] = Field(
        None, description="The direction to order cryptocurrency results."
    )
    cryptocurrency_type: Optional[CryptoCurrencyType] = Field(
        CryptoCurrencyType.ALL, description="The type of cryptocurrency."
    )
    tag: Optional[ListingTag] = Field(
        ListingTag.ALL, description="The tag of cryptocurrency to include."
    )
    aux: Optional[List[ListingAux]] = Field(
        default=[
            ListingAux.NUM_MARKET_PAIRS,
            ListingAux.CMC_RANK,
            ListingAux.DATE_ADDED,
            ListingAux.TAGS,
            ListingAux.PLATFORM,
            ListingAux.MAX_SUPPLY,
            ListingAux.CIRCULATING_SUPPLY,
            ListingAux.TOTAL_SUPPLY,
        ],
        description="Optionally specify a comma-separated list of supplemental data fields to return. Pass 'platform,max_supply,circulating_supply,total_supply,cmc_rank,date_added,tags,num_market_pairs,notice,status' to include all auxiliary fields.",
    )

    # noinspection PyNestedDecorators
    @field_serializer("convert", "aux")
    @classmethod
    def serialize(cls, value: List) -> Optional[str]:
        """
        Serialize the value.
        :param value: The value.
        :return:
        """

        if value is None:
            return None

        return ",".join(value)


class CryptoCurrenciesQuoteParams(BaseModel):
    """
    The parameters for the `/cryptocurrency/quotes` endpoints.
    """

    id: Optional[List[int]] = Field(
        default=None,
        description="A comma-separated list of cryptocurrency IDs to return data for.",
    )
    slug: Optional[List[str]] = Field(
        default=None,
        description="A comma-separated list of cryptocurrency slugs to return data for.",
    )
    symbol: Optional[List[Symbol]] = Field(
        default=None,
        description="A comma-separated list of cryptocurrency symbols to return data for.",
    )
    convert: Optional[str] = Field(
        default=None,
        description="Optionally calculate market quotes in up to 120 currencies at once by passing a comma-separated list of cryptocurrency or fiat currency symbols. Each additional convert option beyond the first requires an additional call credit.",
    )
    convert_id: Optional[str] = Field(
        default=None,
        description="Optionally calculate market quotes by CoinMarketCap ID instead of symbol. This option is identical to convert but uses CoinMarketCap IDs instead of symbols.",
    )
    aux: Optional[List[QuoteAux]] = Field(
        default=[
            QuoteAux.NUM_MARKET_PAIRS,
            QuoteAux.CMC_RANK,
            QuoteAux.DATE_ADDED,
            QuoteAux.TAGS,
            QuoteAux.PLATFORM,
            QuoteAux.MAX_SUPPLY,
            QuoteAux.CIRCULATING_SUPPLY,
            QuoteAux.TOTAL_SUPPLY,
            QuoteAux.MARKET_CAP_BY_TOTAL_SUPPLY,
            QuoteAux.VOLUME_24H_REPORTED,
            QuoteAux.VOLUME_7D,
            QuoteAux.VOLUME_7D_REPORTED,
            QuoteAux.VOLUME_30D,
            QuoteAux.VOLUME_30D_REPORTED,
        ],
        description="Optionally specify a comma-separated list of supplemental data fields to return. Pass 'platform,max_supply,circulating_supply,total_supply,cmc_rank,date_added,tags,num_market_pairs,notice,status' to include all auxiliary fields.",
    )
    skip_invalid: Optional[bool] = Field(
        default=True,
        description="Whether to skip cryptocurrencies that throw an error rather than throwing an error and stopping the request.",
    )

    # noinspection PyNestedDecorators
    @field_serializer("id", "slug", "symbol", "aux")
    @classmethod
    def serialize(cls, value: List) -> Optional[str]:
        """
        Serialize the value.
        :param value: The value.
        :return:
        """

        if value is None:
            return None

        return ",".join(value)
