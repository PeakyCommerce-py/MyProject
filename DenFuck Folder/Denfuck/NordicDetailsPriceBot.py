import requests

# URL for Prisjakts BFF endpoint
url = "https://www.prisjakt.nu/_internal/bff"

# Headers with necessary cookies and user-agent (make sure to update these)
headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    # Add your cookies and user-agent here
}

# Telegram bot API details
telegram_bot_token = "7747077373:AAGYkKIA1TPNxJ4C2P4LbESVRvUSKZBYf5s"
telegram_chat_id = "1148095852"  # Replace with the actual chat ID where you want to send the message

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

# Function to send messages to Telegram
def send_to_telegram(message):
    telegram_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": telegram_chat_id,
        "text": message,
        "parse_mode": "MarkdownV2"  # Allows MarkdownV2 formatting for nicer message formatting
    }
    response = requests.post(telegram_url, json=payload)
    if response.status_code != 200:
        print(f"Failed to send message to Telegram: {response.text}")

# Main logic to get offers and send details to Telegram
product_ids = [10837380]  # Replace with actual product IDs

for product_id in product_ids:
    offers = fetch_product_offers(product_id)
    # Start building the message with the product ID
    message = f"*Offers for Product ID {product_id}:*\n"

    for offer in offers:
        store_name = offer['store']['name'].replace('-', '\\-')
        featured_status = "Yes" if offer['store']['featured'] else "No"
        currency = offer['store']['currency']
        price_excl_shipping = offer['price']['exclShipping']
        in_stock = offer['stock']['status'] == "in_stock"

        # Add details for each offer, making sure to escape necessary characters
        message += (
            f"\n*Store\\:* {store_name}\n\n"
            
            f"*Price\\:* *{price_excl_shipping} {currency}*\n\n"  # Price is bold
            
            f"*Link to Store\\:* [Click Here]({offer['externalUri']})\n\n"
            
            f"*In Stock\\:* {'Yes' if in_stock else 'No'}\n\n"
            
            f"*Featured\\:* {featured_status}\n\n"
            + "\\-" * 40 + "\n"  # MarkdownV2 requires escaping for '-'
        )

    # Send the constructed message to Telegram
    send_to_telegram(message)
