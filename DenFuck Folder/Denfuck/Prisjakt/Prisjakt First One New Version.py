import csv
import requests
import time
import random

# URL for Prisjakt API endpoint
url = "https://www.prisjakt.nu/_internal/bff"

# Headers with necessary cookies and user-agent
headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    # Add your cookies and user-agent here
}

# Function to fetch Product ID for a given EAN
def fetch_product_id(ean):
    payload = {
        "query": """
        query searchPage($query: String!) {
            newSearch(query: $query) {
                results {
                    products {
                        nodes {
                            ... on Product {
                                id
                            }
                        }
                    }
                }
            }
        }
        """,
        "variables": {"query": ean}
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        products = data.get('data', {}).get('newSearch', {}).get('results', {}).get('products', {}).get('nodes', [])
        if products:
            return products[0]['id']
    return None

# Function to fetch offers for a given Product ID
# Function to fetch offers for a given Product ID
def fetch_price_and_merchant_info(product_id):
    payload = {
        "operationName": "productPage",
        "query": """
        query productPage($id: Int!) {
            product(id: $id) {
                prices {
                    nodes {
                        shopOfferId
                        name
                        price {
                            exclShipping
                            inclShipping
                        }
                        stock {
                            status
                            statusText
                        }
                        store {
                            name
                            featured
                        }
                        offerPrices {
                            originalPrice {
                                inclShipping
                            }
                        }
                    }
                }
            }
        }
        """,
        "variables": {"id": product_id}
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        offers = data.get('data', {}).get('product', {}).get('prices', {}).get('nodes', [])
        results = []
        for offer in offers:
            price = offer['price']['inclShipping']
            # Handle potential None cases for original price
            original_price = None
            if offer.get('offerPrices') and offer['offerPrices'].get('originalPrice'):
                original_price = offer['offerPrices']['originalPrice']['inclShipping']

            store_name = offer['store']['name']
            featured = "Yes" if offer['store']['featured'] else "No"
            stock_status = offer['stock']['status']
            results.append({
                'store_name': store_name,
                'price': price,
                'original_price': original_price if original_price else "N/A",
                'featured': featured,
                'stock_status': stock_status
            })
        return results
    return None


# Main logic to fetch Product IDs and offers for each EAN
input_filename = "inputmargin.csv"  # Input CSV with 'EAN', 'Price exc VAT', 'Rec Price'
ean_output_filename = "EAN_ProductID_Sheet.csv"  # Output for EAN and Product IDs
offers_output_filename = "Offers_Sheet.csv"  # Output for offers

# Read input CSV and prepare output files
with open(input_filename, mode="r", encoding="utf-8") as infile, \
     open(ean_output_filename, mode="w", newline="", encoding="utf-8") as ean_file, \
     open(offers_output_filename, mode="w", newline="", encoding="utf-8") as offers_file:

    reader = csv.DictReader(infile)
    ean_fieldnames = reader.fieldnames + ["Product ID"]
    ean_writer = csv.DictWriter(ean_file, fieldnames=ean_fieldnames)
    ean_writer.writeheader()

    offers_fieldnames = ["Product ID", "EAN", "Store", "Price", "Original Price", "Featured", "Stock Status"]
    offers_writer = csv.DictWriter(offers_file, fieldnames=offers_fieldnames)
    offers_writer.writeheader()

    for row in reader:
        ean = row["EAN"]
        print(f"Fetching Product ID for EAN: {ean}")
        product_id = fetch_product_id(ean)

        if product_id:
            # Update and write EAN and Product ID to the first sheet
            row.update({"Product ID": product_id})
            ean_writer.writerow(row)

            # Fetch and write offers to the second sheet
            print(f"Fetching offers for Product ID: {product_id}")
            offers = fetch_price_and_merchant_info(product_id)
            if offers:
                for offer in offers:
                    offers_writer.writerow({
                        "Product ID": product_id,
                        "EAN": ean,
                        "Store": offer['store_name'],
                        "Price": offer['price'],
                        "Original Price": offer['original_price'] if offer['original_price'] else "N/A",
                        "Featured": offer['featured'],
                        "Stock Status": offer['stock_status']
                    })
        else:
            # No Product ID found for this EAN
            print(f"No Product ID found for EAN: {ean}")
            row.update({"Product ID": "No Product Found"})
            ean_writer.writerow(row)

        # Random delay to prevent detection
        delay = random.randint(1, 3)
        print(f"Sleeping for {delay} seconds to avoid detection.")
        time.sleep(delay)

print("EAN and offers have been saved to separate CSV files.")
