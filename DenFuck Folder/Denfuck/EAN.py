import requests
import time
import random

# URLs for API endpoints
search_url = "https://www.pricerunner.se/se/api/search-compare-gateway/public/search/v5/SE?q={EAN}"
product_detail_url = "https://www.pricerunner.se/se/api/search-compare-gateway/public/product-detail/v0/offers/SE/{ID}?af_ORIGIN=NATIONAL&af_ITEM_CONDITION=NEW,UNKNOWN&sortByPreset=PRICE"

# Headers for requests
headers = {
    "accept": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
}


def fetch_product_id(ean):
    """Fetch product ID from EAN."""
    response = requests.get(search_url.format(EAN=ean), headers=headers)
    time.sleep(random.uniform(0, 3))  # Sleep for a random time between 0 and 1 second

    if response.status_code == 200:
        data = response.json()
        products = data.get("products", [])
        if products:
            return products[0]["id"]  # Return the first product ID found
    else:
        print(f"Failed to retrieve product ID for EAN: {ean}. Status code: {response.status_code}")
    return None


def fetch_price_and_merchant_info(product_id):
    """Fetch unique offers (price and merchant) for a given product ID, only if available and in stock."""
    url = product_detail_url.format(ID=product_id)
    response = requests.get(url, headers=headers)
    time.sleep(random.uniform(0, 4))  # Sleep for a random time between 0 and 1 second

    offers_list = []

    if response.status_code == 200:
        data = response.json()
        offers = data.get("offers", [])

        if offers:
            displayed_merchants = set()
            for offer in offers:
                # Check if the offer is available and in stock
                if offer.get("availability") == "AVAILABLE" and offer.get("stockStatus") == "IN_STOCK":
                    price_info = offer.get("price", {})
                    price = price_info.get("amount", "N/A")
                    currency = price_info.get("currency", "N/A")

                    merchant_id = offer.get("merchantId")
                    merchant_name = data["merchants"].get(str(merchant_id), {}).get("name", "Unknown Merchant")

                    if merchant_name not in displayed_merchants:
                        offers_list.append(f" - Merchant: {merchant_name}, Price: {price} {currency}")
                        displayed_merchants.add(merchant_name)
        else:
            offers_list.append("No available in-stock offers found.")
    else:
        print(f"Failed to retrieve details for Product ID {product_id}. Status code: {response.status_code}")

    return offers_list


def main():
    with open("ean_list.txt", "r") as file:
        eans = [line.strip() for line in file if line.strip()]

    for ean in eans:
        print(f"\nFetching offers for EAN: {ean}")
        product_id = fetch_product_id(ean)

        if product_id:
            offers = fetch_price_and_merchant_info(product_id)
            print(f"Offers for Product ID {product_id}:")
            for offer in offers:
                print(offer)
        else:
            print(f"Product ID not found for EAN: {ean}")


if __name__ == "__main__":
    main()
