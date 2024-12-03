import requests
import csv
import time

# URL for Prisjakts BFF endpoint
url = "https://www.prisjakt.nu/_internal/bff"

# Headers with necessary cookies and user-agent (make sure to update these)
headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    # Add your cookies and user-agent here
}

# Function to search for products by EAN
def search_product_by_ean(ean):
    payload = {
        "query": """
        query searchPage($query: String!) {
            newSearch(query: $query) {
                results {
                    products {
                        nodes {
                            ... on Product {
                                id
                                name
                                media {
                                    first(width: _280)
                                }
                                priceSummary {
                                    regular
                                }
                            }
                            ... on Offer {
                                offerId
                                name
                                externalUri
                                media {
                                    first
                                }
                                store {
                                    name
                                    id
                                    featured
                                    currency
                                }
                                offerPrice {
                                    regular
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
            return data['data']['newSearch']['results']['products']['nodes']
        else:
            print(f"No valid data found for EAN {ean}: {data}")
            return []
    else:
        print(f"Error fetching product for EAN {ean}: {response.text}")
        return []

# Function to load EANs from a text file
def load_eans_from_file(filename):
    try:
        with open(filename, 'r') as file:
            ean_list = [line.strip() for line in file if line.strip()]  # Remove whitespace and empty lines
        return ean_list
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

# Main logic to search for each EAN and save details to a CSV
def main():
    input_filename = "ean_list.txt"  # Input file containing EANs
    output_filename = "ean_offers_with_details.csv"  # Output file for results
    delay_between_requests = 2  # Delay in seconds between requests

    # Load EANs from the input file
    ean_list = load_eans_from_file(input_filename)

    # Prepare the CSV file for writing results
    with open(output_filename, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["EAN", "Store", "Price", "Product ID", "Featured", "Offer ID"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Process each EAN
        for ean in ean_list:
            print(f"\nSearching for EAN: {ean}")
            products = search_product_by_ean(ean)

            if products:
                for product in products:
                    if 'id' in product:  # Check if it's a Product
                        print(f"Product Found: ID: {product['id']}, Name: {product['name']}")
                        writer.writerow({
                            "EAN": ean,
                            "Store": "N/A",
                            "Price": "N/A",
                            "Product ID": product["id"],
                            "Featured": "N/A",
                            "Offer ID": "N/A"
                        })
                    if 'offerId' in product:  # Check if it's an Offer
                        store_name = product['store']['name']
                        price = product['offerPrice']['regular']
                        offer_id = product['offerId']
                        featured_status = "Yes" if product['store']['featured'] else "No"
                        print(f"Offer Found: Store: {store_name}, Price: {price}, Offer ID: {offer_id}")
                        writer.writerow({
                            "EAN": ean,
                            "Store": store_name,
                            "Price": price,
                            "Product ID": "N/A",
                            "Featured": featured_status,
                            "Offer ID": offer_id
                        })
            else:
                print(f"No products or offers found for EAN: {ean}")
                writer.writerow({
                    "EAN": ean,
                    "Store": "No Store Found",
                    "Price": "N/A",
                    "Product ID": "N/A",
                    "Featured": "N/A",
                    "Offer ID": "N/A"
                })

            # Introduce a delay between requests
            time.sleep(delay_between_requests)

    print(f"\nResults have been saved to {output_filename}")

if __name__ == "__main__":
    main()
