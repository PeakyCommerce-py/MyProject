import requests  # Make sure to import requests

# URL for Prisjakts BFF endpoint
url = "https://www.prisjakt.nu/_internal/bff"

# Headers with necessary cookies and user-agent
headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    # Add your cookies and user-agent here
}


# Function to fetch offers for a given product ID
def fetch_product_offers(product_id):
    payload = {
        "operationName": "productPage",
        "query": """
        query productPage($id: Int!) {
            product(id: $id) {
                prices {
                    nodes {
                        shopOfferId
                        name
                        externalUri
                        price {
                            inclShipping
                            exclShipping
                        }
                        store {
                            name
                            currency
                            featured
                        }
                        stock {
                            status
                            statusText
                        }
                    }
                }
            }
        }
        """,
        "variables": {
            "id": product_id
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'product' in data['data']:
            return data['data']['product']['prices']['nodes']
        else:
            print(f"No valid offer data found for Product ID {product_id}: {data}")
            return []
    else:
        print(f"Error fetching offers for Product ID {product_id}: {response.text}")
        return []

# Main logic to get offers and print details
product_ids = [13994834]  # Replace with actual product IDs

for product_id in product_ids:
    offers = fetch_product_offers(product_id)
    print(f"\nOffers for Product ID {product_id}:")

    for offer in offers:
        store_name = offer['store']['name']
        featured_status = "Yes" if offer['store']['featured'] else "No"
        currency = offer['store']['currency']
        price_incl_shipping = offer['price']['inclShipping']
        price_excl_shipping = offer['price']['exclShipping']
        in_stock = offer['stock']['status'] == "in_stock"

        print(f"Store: {store_name}")
        print(f"Price (Excl. Shipping): {price_excl_shipping} {currency}")
        print(f"Price (Incl. Shipping): {price_incl_shipping} {currency}")
        print(f"Link to Store: {offer['externalUri']}")
        print(f"In Stock: {'Yes' if in_stock else 'No'}")
        print(f"Featured: {featured_status}")
        print("-" * 40)