"""
cryptocurrencies.py This file contains the routes of the /cryptocurrency routes.
"""

from cryptopi import CoinMarketCapApi
from cryptopi.api.urls.responses import QuoteResponse
from cryptopi.models import Symbol
from cryptopi.utils import find_api_key

from typing import Optional
from fastapi import APIRouter

router = APIRouter(
    prefix="/cryptocurrency",
)


@router.get("/quotes/latest")
async def get_latest_quotes(symbol: Optional[list[str]] = None) -> QuoteResponse:
    """
    This function returns the latest quotes of all cryptocurrencies.
    :return:
    """

    # Get the API key.
    api_key = find_api_key()

    # Create the API instance.
    api = CoinMarketCapApi(api_key=api_key)

    # Load the symbols.
    symbols = [Symbol(symbol) for symbol in symbol] if symbol else None

    # Define the params.
    params = {}
    if symbols:
        params["symbol"] = symbols

    # Get the latest quotes.
    return api.cryptocurrency_latest_quotes()
