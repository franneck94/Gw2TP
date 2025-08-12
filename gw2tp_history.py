from __future__ import annotations

from typing import Any
from typing import Dict

import httpx


class GW2API:
    """Client for interacting with GW2 API"""

    BASE_URL_LISTINGS = "https://api.guildwars2.com/v2/commerce/listings"
    BASE_URL_PRICES = "https://api.guildwars2.com/v2/commerce/prices"

    def __init__(self) -> GW2API:
        self.session = httpx.Client()

    def get_listings(self, item_id: int) -> Dict[str, Any]:
        """Get current buy and sell listings for an item"""
        response = self.session.get(
            f"{self.BASE_URL_LISTINGS}/{item_id}",
            timeout=10.0,
        )
        response.raise_for_status()
        return response.json()

    def get_prices(self, item_id: int) -> Dict[str, Any]:
        """Get current buy and sell prices for an item"""
        response = self.session.get(
            f"{self.BASE_URL_PRICES}/{item_id}",
            timeout=10.0,
        )
        response.raise_for_status()
        return response.json()


# Example usage:
if __name__ == "__main__":
    client = GW2API()
    ecto_id = 19721

    try:
        ecto_listings = client.get_listings(ecto_id)

        print("\nBuy Orders:")
        for buy in ecto_listings["buys"][:5]:  # Show first 5 orders
            print(
                f"Quantity: {buy['quantity']}, Price: {buy['unit_price']} copper",
            )

        print("\nSell Orders:")
        for sell in ecto_listings["sells"][:5]:  # Show first 5 orders
            print(
                f"Quantity: {sell['quantity']}, Price: {sell['unit_price']} copper",
            )
    except httpx.HTTPError as e:
        print(f"Error fetching data: {e}")

    try:
        ecto_listings = client.get_prices(ecto_id)
    except httpx.HTTPError as e:
        print(f"Error fetching data: {e}")
