"""
data.py Contains Enums for the API data responses.
"""
from enum import Enum
from typing import Final


class DefaultEnum:
    """
    The default Mixin.
    """

    UNKNOWN: Final[str] = "UNKNOWN"


class FiatCurrency(str, Enum):
    """
    The fiat currency.
    """

    USD: Final[str] = "USD"


class Symbol(str, Enum):
    """
    The symbol for a cryptocurrency.
    """

    # Default
    UNKNOWN: Final[str] = DefaultEnum.UNKNOWN

    BTC: Final[str] = "BTC"
    ETH: Final[str] = "ETH"
    XLM: Final[str] = "XLM"
    AVAX: Final[str] = "AVAX"
    LINK: Final[str] = "LINK"
    BCH: Final[str] = "BCH"

    @classmethod
    def _missing_(cls, value):
        """
        Return the default value.
        :param value: The value.
        :return:
        """

        return cls.UNKNOWN


class SymbolName(str, Enum):
    """
    The name for a cryptocurrency.
    """

    # Default
    UNKNOWN: Final[str] = DefaultEnum.UNKNOWN

    BITCOIN: Final[str] = "Bitcoin"
    ETHEREUM: Final[str] = "Ethereum"
    STELLAR: Final[str] = "Stellar"
    AVALANCHE: Final[str] = "Avalanche"
    CHAINLINK: Final[str] = "Chainlink"
    BITCOIN_CASH: Final[str] = "Bitcoin Cash"

    @classmethod
    def _missing_(cls, value):
        """
        Return the default value.
        :param value: The value.
        :return:
        """

        return cls.UNKNOWN


class SymbolSlug(str, Enum):
    """
    The slug for a cryptocurrency.
    """

    # Default
    UNKNOWN: Final[str] = DefaultEnum.UNKNOWN

    BITCOIN: Final[str] = "bitcoin"
    ETHEREUM: Final[str] = "ethereum"
    STELLAR: Final[str] = "stellar"
    AVALANCHE: Final[str] = "avalanche"
    CHAINLINK: Final[str] = "chainlink"
    BITCOIN_CASH: Final[str] = "bitcoin-cash"

    @classmethod
    def _missing_(cls, value):
        """
        Return the default value.
        :param value: The value.
        :return:
        """

        return cls.UNKNOWN
