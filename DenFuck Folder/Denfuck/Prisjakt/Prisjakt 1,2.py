import requests
import csv

# URL for Prisjakts BFF endpoint
url = "https://www.prisjakt.nu/_internal/bff"

# Headers with necessary cookies and user-agent
headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    # Add your cookies and user-agent here
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
}

# Function to search for products by EAN and fetch offers for a given product ID
def search_product_by_ean_and_fetch_offers(ean):
    payload = {
        "query": """
        query searchPage($query: String!) {
            newSearch(query: $query) {
                results {
                    products {
                        nodes {
                            ... on Product {
                                id
                                prices {
                                    nodes {
                                        shopOfferId
                                        price {
                                            exclShipping
                                        }
                                        store {
                                            name
                                            featured
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        """,
        "variables": {
            "query": ean
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'newSearch' in data['data']:
            products = data['data']['newSearch']['results']['products']['nodes']
            return products
        else:
            print(f"No valid data found for EAN {ean}: {data}")
            return []
    else:
        print(f"Error fetching product for EAN {ean}: {response.text}")
        return []

# Function to fetch offers for a given product ID
def fetch_offers_by_product_id(product_id):
    payload = {
        "query": """
        query productPage($id: Int!) {
            product(id: $id) {
                prices {
                    nodes {
                        shopOfferId
                        price {
                            exclShipping
                        }
                        store {
                            name
                            featured
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

# Main logic to load product IDs from CSV and fetch offers
def main():
    input_filename = "ean_list.txt"  # Input file from previous script
    output_filename = "product_offers_done.csv"  # Output file with all offers

    # Load EANs from the text file
    products = []
    with open(input_filename, mode="r", encoding="utf-8") as file:
        ean_list = [line.strip() for line in file if line.strip()]
        for ean in ean_list:
            products.append({"EAN": ean})

    # Define fieldnames for output CSV
    fieldnames = ["EAN", "Store Name", "Sell Price", "Featured", "Offer ID"]

    with open(output_filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for product in products:
            ean = product["EAN"]
            # Search for products by EAN and get both product details and offers
            products_data = search_product_by_ean_and_fetch_offers(ean)

            if products_data:
                # First, write offers from the initial EAN search
                for product_data in products_data:
                    product_id = product_data.get("id")
                    offers = product_data.get("prices", {}).get("nodes", [])

                    if offers:
                        for offer in offers:
                            # Skip offers that do not have valid data
                            if not offer.get('price') or not offer.get('store') or not offer.get('shopOfferId'):
                                continue

                            # Update the base data with offer-specific information
                            row = {
                                "EAN": ean,
                                "Store Name": offer['store']['name'],
                                "Sell Price": offer['price']['exclShipping'],
                                "Featured": "Yes" if offer['store']['featured'] else "No",
                                "Offer ID": offer.get("shopOfferId", "No Offer ID")
                            }
                            # Write each offer to the file
                            writer.writerow(row)
                            print(f"EAN Offer - Store: {row['Store Name']}, Price (Excl. Shipping): {row['Sell Price']}, Featured: {row['Featured']}, Offer ID: {row['Offer ID']}")

                    # If a Product ID was found, use it to fetch additional offers
                    if product_id:
                        additional_offers = fetch_offers_by_product_id(product_id)

                        if additional_offers:
                            for offer in additional_offers:
                                # Skip offers that do not have valid data
                                if not offer.get('price') or not offer.get('store') or not offer.get('shopOfferId'):
                                    continue

                                # Update the base data with offer-specific information
                                row = {
                                    "EAN": ean,
                                    "Store Name": offer['store']['name'],
                                    "Sell Price": offer['price']['exclShipping'],
                                    "Featured": "Yes" if offer['store']['featured'] else "No",
                                    "Offer ID": offer.get("shopOfferId", "No Offer ID")
                                }
                                # Write each additional offer to the file
                                writer.writerow(row)
                                print(f"Product ID Offer - Store: {row['Store Name']}, Price (Excl. Shipping): {row['Sell Price']}, Featured: {row['Featured']}, Offer ID: {row['Offer ID']}")

if __name__ == "__main__":
    main()
