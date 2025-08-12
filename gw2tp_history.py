from typing import Any
from typing import Dict

import httpx


class GW2API:
    """Client for interacting with GW2 API"""

    BASE_URL = "https://api.guildwars2.com/v2/commerce/listings"

    def __init__(self):
        self.session = httpx.Client()

    def get_listings(self, item_id: int) -> Dict[str, Any]:
        """Get current buy and sell listings for an item

        Args:
            item_id: The item ID to get listings for

        Returns:
            Dict containing buy and sell orders with quantities and prices
        """
        response = self.session.get(f"{self.BASE_URL}/{item_id}", timeout=10.0)
        response.raise_for_status()
        return response.json()


# Example usage:
if __name__ == "__main__":
    client = GW2API()

    # Get listings for Glob of Ectoplasm (ID: 19721)
    try:
        ecto_listings = client.get_listings(19721)

        # Print buy orders
        print("\nBuy Orders:")
        for buy in ecto_listings["buys"][:5]:  # Show first 5 orders
            print(
                f"Quantity: {buy['quantity']}, Price: {buy['unit_price']} copper"
            )

        # Print sell orders
        print("\nSell Orders:")
        for sell in ecto_listings["sells"][:5]:  # Show first 5 orders
            print(
                f"Quantity: {sell['quantity']}, Price: {sell['unit_price']} copper"
            )

    except httpx.HTTPError as e:
        print(f"Error fetching data: {e}")
