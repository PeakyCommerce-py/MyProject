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
            products = data['data']['newSearch']['results']['products']['nodes']
            return products
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

# Main logic to search for each EAN from the text file and print product details and offers
ean_list = load_eans_from_file("ean_list.txt")  # Load EANs from the file

for ean in ean_list:
    print(f"Searching for EAN: {ean}")
    products = search_product_by_ean(ean)

    for product in products:
        if 'id' in product:  # Check if it's a Product
            print("-" * 40)
            print(f"Found Product: {product['name']} (ID: {product['id']})")
            print("-" * 40)
        if 'offerId' in product:  # Check if it's an Offer
            featured_status = "Yes" if product['store']['featured'] else "No"
            print(f"Produkt Namn |: {product['name']}")
            print(f"Store |: {product['store']['name']} (Featured: {featured_status})")
            print(f"Price |: {product['offerPrice']['regular']} {product['store']['currency']}")
            print(f"Link to Store |: {product['externalUri']}")
            print("-" * 40)

    if not products:
        print(f"No products found for EAN {ean}.")
