import logging

import requests
from requests.exceptions import HTTPError


class Trading212:
    """Rest API client for Trading212"""

    def __init__(self, api_key: str, demo: bool = True):
        """ """
        self.api_key = api_key
        self.host = (
            "https://live.trading212.com" if demo else "https://live.trading212.com"
        )

    def _get(self, endpoint: str, params=None, api_version: str = "v0"):
        return self._process_response(
            requests.get(
                f"{self.host}/api/{api_version}/{endpoint}",
                headers={"Authorization": self.api_key},
                params=params,
            )
        )

    def _get_url(
        self,
        url,
    ):
        return self._process_response(
            requests.get(
                f"{self.host}/{url}",
                headers={"Authorization": self.api_key},
            )
        )

    @staticmethod
    def _process_response(resp):
        try:
            resp.raise_for_status()
        except HTTPError as http_err:
            logging.error(resp.text)
            raise http_err

        return resp.json()

    def _process_items(self, response):
        res = []
        res += response["items"]
        while next_page := response.get("nextPagePath"):
            response = self._get_url(next_page)
            res += response["items"]

        return res

    def orders(self, cursor: int = 0, ticker: str = None, limit: int = 50):
        """Historical order data"""

        params = {"cursor": cursor, "limit": limit}
        if ticker:
            params["ticker"] = ticker

        return self._process_items(self._get("equity/history/orders", params=params))

    def dividends(self, cursor: int = 0, ticker: str = None, limit: int = 50):
        """Dividends paid out"""

        params = {"cursor": cursor, "limit": limit}
        if ticker:
            params["ticker"] = ticker

        return self._process_items(self._get("history/dividends", params=params))

    def transactions(self, cursor: int = 0, limit: int = 50):
        """Transactions list"""

        params = {"cursor": cursor, "limit": limit}

        return self._process_items(self._get("history/transactions", params=params))

    def instruments(self):
        """Tradeable instruments metadata"""
        return self._get("equity/metadata/instruments")

    def cash(self):
        """Account cash"""
        return self._get("equity/account/cash")

    def portfolio(self):
        """All open positions"""
        return self._get("equity/portfolio")
