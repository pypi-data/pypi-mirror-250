"""
interface.py This file contains the CryptoCurrencyUrl class for the API.
"""
from urllib.parse import urljoin

import cmc.api.urls.paths as paths


class CryptoCurrencyUrl:
    """
    The ``CryptoCurrencyUrl`` class represents a CryptoCurrencyUrl.
    """

    def __init__(self, sandbox: bool = False):
        """
        Initializes the ``CryptoCurrencyUrl`` instance.
        """

        self._sandbox = sandbox

    @property
    def sandbox(self):
        """
        Return whether the CryptoCurrencyUrl is for the sandbox.
        :return:
        """

        return self._sandbox

    @property
    def base_url(self):
        """
        Return the base CryptoCurrencyUrl.
        :return:
        """

        if self.sandbox:
            return paths.BaseUrl.SANDBOX
        return paths.BaseUrl.PRODUCTION

    @property
    def map(self):
        """
        Return the CryptoCurrencyUrl for the `/cryptocurrency/listings/latest` endpoint.
        :return:
        """

        # noinspection PyTypeChecker
        return urljoin(
            self.base_url, urljoin(paths.ApiVersion.V1, paths.CryptoCurrencyPaths.MAP)
        )

    # noinspection PyTypeChecker
    @property
    def latest_listings(self, latest: bool = True):
        """
        Return the CryptoCurrencyUrl for the `/cryptocurrency/listings` endpoint.
        :return:
        """

        return urljoin(
            self.base_url,
            urljoin(paths.ApiVersion.V1, paths.CryptoCurrencyPaths.LISTINGS_LATEST),
        )

    # noinspection PyTypeChecker
    @property
    def latest_quotes(self, latest: bool = True):
        """
        Return the CryptoCurrencyUrl for the `/cryptocurrency/quotes` endpoint.
        :return:
        """

        return urljoin(
            self.base_url,
            urljoin(paths.ApiVersion.V1, paths.CryptoCurrencyPaths.QUOTES_LATEST),
        )
