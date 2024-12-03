import requests
import csv

# URL for Prisjakts BFF endpoint
url = "https://www.prisjakt.nu/_internal/bff"

# Headers with necessary cookies and user-agent
headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
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

# Main logic to process the EAN results and fetch offers
def main():
    input_filename = "ean_offers_with_details.csv"  # Input file with EAN and Product IDs
    output_filename = "Prisjakt_Bergspotter.csv"  # Output file for offers

    with open(input_filename, mode="r", encoding="utf-8") as infile, open(output_filename, mode="w", newline="", encoding="utf-8") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ["EAN", "Store", "Price", "Product ID", "Featured", "In Stock", "Offer ID"]  # Final output fields
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            ean = row["EAN"]
            product_id = row.get("Product ID")
            existing_store = row.get("Store", "N/A")
            existing_price = row.get("Price", "N/A")
            existing_featured = row.get("Featured", "N/A")
            existing_in_stock = row.get("In Stock", "N/A")

            # Write the existing row if it contains "EAN Search" data
            if existing_store != "N/A":
                writer.writerow({
                    "EAN": ean,
                    "Store": existing_store,
                    "Price": existing_price,
                    "Product ID": product_id,
                    "Featured": existing_featured,
                    "In Stock": existing_in_stock,
                    "Offer ID": "N/A"  # No Offer ID for EAN Search data
                })

            # Skip invalid Product IDs but keep the original row
            if not product_id or product_id == "N/A":
                print(f"Skipping EAN {ean} due to invalid Product ID: {product_id}")
                continue

            print(f"Fetching offers for Product ID: {product_id}")

            offers = fetch_product_offers(int(product_id))
            if offers:
                for offer in offers:
                    store_name = offer['store']['name']
                    featured_status = "Yes" if offer['store']['featured'] else "No"
                    selling_price = offer['price']['exclShipping']  # Excluding shipping price
                    in_stock = "Yes" if offer['stock']['status'] == "in_stock" else "No"
                    offer_id = offer.get("shopOfferId", "No Offer ID")

                    # Write a new row for each offer
                    writer.writerow({
                        "EAN": ean,
                        "Store": store_name,
                        "Price": selling_price,
                        "Product ID": product_id,
                        "Featured": featured_status,
                        "In Stock": in_stock,
                        "Offer ID": offer_id  # Add Offer ID to the output
                    })

    print(f"Offers have been saved to {output_filename}")

if __name__ == "__main__":
    main()
