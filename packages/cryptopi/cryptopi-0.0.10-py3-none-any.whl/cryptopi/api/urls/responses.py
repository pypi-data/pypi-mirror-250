"""
responses.py This file contains the models for API responses.
"""
from datetime import datetime
from decimal import Decimal
from typing import Dict
from typing import List
from typing import Optional

from cryptopi.api.urls.data import FiatCurrency
from cryptopi.api.urls.data import Symbol
from cryptopi.api.urls.data import SymbolName
from cryptopi.api.urls.data import SymbolSlug
from cryptopi.api.urls.utils import format_date_string
from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator


class BaseResponse(BaseModel):
    """
    The base response model.
    """

    def as_dict(self):
        """
        Return the dictionary representation.
        :return:
        """

        return self.model_dump()


class ResponseStatus(BaseResponse):
    """
    The status model for the `/cryptocurrency/map` endpoint.
    """

    timestamp: datetime = Field(..., description="The timestamp for the response.")
    error_code: int = Field(..., description="The error code for the response.")
    error_message: Optional[str] = Field(
        None, description="The error message for the response."
    )
    elapsed: int = Field(..., description="The elapsed time for the response.")
    credit_count: int = Field(..., description="The credit count for the response.")
    notice: Optional[str] = Field(None, description="The notice for the response.")

    # noinspection PyNestedDecorators
    @field_validator("timestamp")
    @classmethod
    def validate_timestamp(cls, value: str) -> Optional[datetime]:
        """
        Validate the timestamp.
        :param value: The value.
        :return:
        """

        return format_date_string(value)


class ResponsePlatform(BaseResponse):
    """
    The platform model for the `/cryptocurrency/listings` endpoints.
    """

    id: int = Field(..., description="The CoinMarketCap ID for the platform.")
    name: SymbolName = Field(..., description="The name for the symbol.")
    symbol: Symbol = Field(..., description="The symbol for the cryptocurrency.")
    slug: SymbolSlug = Field(..., description="The slug for the cryptocurrency.")
    token_address: str = Field(
        ..., description="The token address for the cryptocurrency."
    )


class MapResponseData(BaseResponse):
    """
    The data model for the `/cryptocurrency/map` endpoint.
    """

    id: int = Field(..., description="The CoinMarketCap ID for the cryptocurrency.")
    rank: int = Field(..., description="The CoinMarketCap rank for the cryptocurrency.")
    symbol: Symbol = Field(..., description="The symbol for the cryptocurrency.")
    name: SymbolName = Field(..., description="The name for the cryptocurrency.")
    slug: SymbolSlug = Field(..., description="The slug for the cryptocurrency.")
    is_active: int = Field(
        ..., description="Whether the cryptocurrency is active on CoinMarketCap."
    )
    platform: Optional[ResponsePlatform] = Field(
        None, description="The platform for the cryptocurrency."
    )

    first_historical_data: Optional[datetime] = Field(
        None,
        description="The first historical data for the cryptocurrency.",
    )
    last_historical_data: Optional[datetime] = Field(
        None, description="The last historical data for the cryptocurrency."
    )

    # noinspection PyNestedDecorators
    @field_validator("first_historical_data", "last_historical_data")
    @classmethod
    def validate_date(cls, value: str) -> Optional[datetime]:
        """
        Validate the date.
        :param value: The value.
        :return:
        """

        return format_date_string(value)


class MapResponse(BaseResponse):
    """
    The response model for the `/cryptocurrency/map` endpoint.
    """

    data: list[MapResponseData] = Field(..., description="The data for the response.")
    status: ResponseStatus = Field(..., description="The status for the response.")


class ResponseQuote(BaseResponse):
    """
    The quote model for the `/cryptocurrency/listings` endpoints.
    """

    price: Optional[Decimal] = Field(
        default=None, description="The price for the cryptocurrency."
    )
    volume_24h: Optional[Decimal] = Field(
        default=None, description="The 24-hour volume for the cryptocurrency."
    )
    volume_change_24h: Optional[Decimal] = Field(
        default=None, description="The 24-hour volume change for the cryptocurrency."
    )
    volume_24h_reported: Optional[Decimal] = Field(
        default=None, description="The reported 24-hour volume for the cryptocurrency."
    )
    volume_7d: Optional[Decimal] = Field(
        default=None, description="The 7-day volume for the cryptocurrency."
    )
    volume_change_7d: Optional[Decimal] = Field(
        default=None, description="The 7-day volume change for the cryptocurrency."
    )
    volume_7d_reported: Optional[Decimal] = Field(
        default=None, description="The reported 7-day volume for the cryptocurrency."
    )
    volume_30d: Optional[Decimal] = Field(
        default=None, description="The 30-day volume for the cryptocurrency."
    )
    volume_change_30d: Optional[Decimal] = Field(
        default=None, description="The 30-day volume change for the cryptocurrency."
    )
    volume_30d_reported: Optional[Decimal] = Field(
        default=None, description="The reported 30-day volume for the cryptocurrency."
    )
    market_cap: Optional[Decimal] = Field(
        default=None, description="The market cap for the cryptocurrency."
    )
    market_cap_dominance: Optional[Decimal] = Field(
        default=None, description="The market cap dominance for the cryptocurrency."
    )
    fully_diluted_market_cap: Optional[Decimal] = Field(
        default=None, description="The fully diluted market cap for the cryptocurrency."
    )
    tvl: Optional[Decimal] = Field(
        default=None, description="The total value locked for the cryptocurrency."
    )
    percent_change_1h: Optional[Decimal] = Field(
        default=None, description="The 1-hour percent change for the cryptocurrency."
    )
    percent_change_24h: Optional[Decimal] = Field(
        default=None, description="The 24-hour percent change for the cryptocurrency."
    )
    percent_change_7d: Optional[Decimal] = Field(
        default=None, description="The 7-day percent change for the cryptocurrency."
    )
    last_updated: datetime = Field(
        ..., description="The last updated timestamp for the cryptocurrency."
    )

    # noinspection PyNestedDecorators
    @field_validator("last_updated")
    @classmethod
    def validate_date(cls, value: str) -> Optional[datetime]:
        """
        Validate the date.
        :param value: The value.
        :return:
        """

        return format_date_string(value)


class ListingResponseData(BaseResponse):
    """
    The data model for the `/cryptocurrency/listings` endpoints.
    """

    id: int = Field(..., description="The CoinMarketCap ID for the cryptocurrency.")
    name: SymbolName = Field(..., description="The name for the cryptocurrency.")
    symbol: Symbol = Field(..., description="The symbol for the cryptocurrency.")
    slug: SymbolSlug = Field(..., description="The slug for the cryptocurrency.")
    cmc_rank: int = Field(
        ..., description="The CoinMarketCap rank for the cryptocurrency."
    )
    num_market_pairs: int = Field(
        ..., description="The number of market pairs for the cryptocurrency."
    )
    circulating_supply: Optional[Decimal] = Field(
        ..., description="The circulating supply for the cryptocurrency."
    )
    total_supply: Optional[Decimal] = Field(
        ..., description="The total supply for the cryptocurrency."
    )
    max_supply: Optional[Decimal] = Field(
        ..., description="The maximum supply for the cryptocurrency."
    )
    infinite_supply: bool = Field(
        ..., description="Whether the cryptocurrency has an infinite supply."
    )
    last_updated: datetime = Field(
        ..., description="The last updated timestamp for the cryptocurrency."
    )
    date_added: Optional[datetime] = Field(
        ..., description="The date added for the cryptocurrency."
    )
    tags: Optional[List[str]] = Field(
        ..., description="The tags for the cryptocurrency."
    )
    platform: Optional[ResponsePlatform] = Field(
        None, description="The platform for the cryptocurrency."
    )
    self_reported_circulating_supply: Optional[Decimal] = Field(
        None, description="The self-reported circulating supply for the cryptocurrency."
    )
    self_reported_market_cap: Optional[Decimal] = Field(
        None, description="The self-reported market cap for the cryptocurrency."
    )
    quote: Dict[Symbol, ResponseQuote] = Field(
        ..., description="The quote for the cryptocurrency."
    )

    # noinspection PyNestedDecorators
    @field_validator("date_added", "last_updated")
    @classmethod
    def validate_date(cls, value: str) -> Optional[datetime]:
        """
        Validate the date.
        :param value: The value.
        :return:
        """

        return format_date_string(value)


class ListingResponse(BaseResponse):
    """
    The response model for the `/cryptocurrency/listings` endpoints.
    """

    data: list[ListingResponseData] = Field(
        ..., description="The data for the response."
    )
    status: ResponseStatus = Field(..., description="The status for the response.")


class QuoteResponseData(BaseResponse):
    """
    The data model for the `/cryptocurrency/quotes` endpoints.
    """

    id: int = Field(..., description="The CoinMarketCap ID for the cryptocurrency.")
    name: SymbolName = Field(..., description="The name for the cryptocurrency.")
    symbol: Symbol = Field(..., description="The symbol for the cryptocurrency.")
    slug: SymbolSlug = Field(..., description="The slug for the cryptocurrency.")
    is_active: Optional[int] = Field(
        default=None,
        description="Whether the cryptocurrency is active on CoinMarketCap.",
    )
    is_fiat: Optional[int] = Field(
        default=None, description="Whether the currency is a fiat currency."
    )
    circulating_supply: Optional[Decimal] = Field(
        default=None, description="The circulating supply for the cryptocurrency."
    )
    total_supply: Optional[Decimal] = Field(
        default=None, description="The total supply for the cryptocurrency."
    )
    date_added: Optional[datetime] = Field(
        default=None, description="The date added for the cryptocurrency."
    )
    last_updated: Optional[datetime] = Field(
        default=None, description="The last updated timestamp for the cryptocurrency."
    )
    num_market_pairs: Optional[int] = Field(
        ..., description="The number of market pairs for the cryptocurrency."
    )
    cmc_rank: Optional[int] = Field(
        ..., description="The CoinMarketCap rank for the cryptocurrency."
    )
    tags: Optional[List[str]] = Field(
        default=None, description="The tags for the cryptocurrency."
    )
    platform: Optional[ResponsePlatform] = Field(
        default=None, description="The platform for the cryptocurrency."
    )
    quote: Dict[FiatCurrency, ResponseQuote] = Field(
        ..., description="The quote for the cryptocurrency."
    )


class QuoteResponse(BaseResponse):
    """
    The response model for the `/cryptocurrency/quotes` endpoints.
    """

    data: Dict[Symbol, QuoteResponseData] = Field(
        ..., description="The data for the response."
    )
    status: ResponseStatus = Field(..., description="The status for the response.")
