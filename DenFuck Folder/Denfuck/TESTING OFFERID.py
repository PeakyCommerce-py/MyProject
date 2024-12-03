import requests
import csv
import time
import re

# URL for Prisjakts BFF endpoint
url = "https://www.prisjakt.nu/_internal/bff"

# Headers with necessary cookies and user-agent (make sure to update these)
headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    # Add your cookies and user-agent here
}

# English to Swedish color translation with prefix handling
color_translation = {
    "Red": "Röd", "Light Red": "Ljusröd", "Dark Red": "Mörkröd",
    "Blue": "Blå", "Light Blue": "Ljusblå", "Dark Blue": "Mörkblå",
    "Yellow": "Gul", "Light Yellow": "Ljusgul", "Dark Yellow": "Mörkgul",
    "Green": "Grön", "Light Green": "Ljusgrön", "Dark Green": "Mörkgrön",
    "Orange": "Orange", "Light Orange": "Ljusorange", "Dark Orange": "Mörkorange",
    "Purple": "Lila", "Light Purple": "Ljuslila", "Dark Purple": "Mörklila",
    "Pink": "Rosa", "Light Pink": "Ljusrosa", "Dark Pink": "Mörkrosa",
    "Brown": "Brun", "Light Brown": "Ljusbrun", "Dark Brown": "Mörkbrun",
    "Black": "Svart",
    "White": "Vit",
    "Gray": "Grå", "Light Gray": "Ljusgrå", "Dark Gray": "Mörkgrå",
    "Turquoise": "Turkos", "Light Turquoise": "Ljusturkos", "Dark Turquoise": "Mörkturkos",
    "Cyan": "Cyan", "Light Cyan": "Ljuscyan", "Dark Cyan": "Mörkcyan",
    "Magenta": "Magenta", "Light Magenta": "Ljusmagenta", "Dark Magenta": "Mörkmagenta",
    "Indigo": "Indigo", "Light Indigo": "Ljusindigo", "Dark Indigo": "Mörkindigo",
    "Violet": "Violett", "Light Violet": "Ljusviolett", "Dark Violet": "Mörkviolett",
    "Gold": "Guld",
    "Silver": "Silver",
    "Beige": "Beige",
    "Ochre": "Ockra",
    "Amber": "Bärnsten",
    "Olive Green": "Olivgrön",
    "Sienna": "Sienna",
    "Sepia": "Sepia",
    "Coral": "Korall",
    "Blush": "Skär",
    "Lavender": "Lavendel",
    "Sage": "Salvia",
    "Teal": "Teal",
    "Maroon": "Maroon",
    "Khaki": "Khaki",
    "Lime": "Lime",
    "Mustard": "Mustard",
    "Navy": "Navy",
    "Emerald": "Smaragd",
    "Sapphire": "Safir",
    "Ruby": "Rubin",
    "Amaranth": "Amarant",
    "Chestnut": "Kastanj",
    "Crimson": "Karmosin",
    "Copper": "Koppar",
    "Bronze": "Bron",
    "Ivory": "Elfenben",
    "Royal Blue": "Kungsblå",
    "Plum": "Plommon",
    "Peach": "Persika",
    "Sand": "Sand",
    "Terracotta": "Terrakotta",
    "Taupe": "Taupe",
    "Ultramarine": "Ultramarin",
    "Cinnabar": "Zinnober"
}

# Swedish basic colors list
swedish_colors = {
    "Röd", "Ljusröd", "Mörkröd", "Blå", "Ljusblå", "Mörkblå", "Gul", "Ljusgul", "Mörkgul",
    "Grön", "Ljusgrön", "Mörkgrön", "Orange", "Ljusorange", "Mörkorange", "Lila", "Ljuslila",
    "Mörklila", "Rosa", "Ljusrosa", "Mörkrosa", "Brun", "Ljusbrun", "Mörkbrun", "Svart",
    "Vit", "Grå", "Ljusgrå", "Mörkgrå", "Turkos", "Ljusturkos", "Mörkturkos", "Cyan",
    "Ljuscyan", "Mörkcyan", "Magenta", "Ljusmagenta", "Mörkmagenta", "Indigo", "Ljusindigo",
    "Mörkindigo", "Violett", "Ljusviolett", "Mörkviolett", "Guld", "Silver", "Beige", "Ockra",
    "Bärnsten", "Olivgrön", "Sienna", "Sepia", "Korall", "Skär", "Lavendel", "Salvia",
    "Teal", "Maroon", "Khaki", "Lime", "Mustard", "Navy", "Smaragd", "Safir", "Rubin",
    "Amarant", "Kastanj", "Karmosin", "Koppar", "Bron", "Elfenben", "Kungsblå", "Plommon",
    "Persika", "Sand", "Terrakotta", "Taupe", "Ultramarin", "Zinnober"
}

# Function to translate color from English to Swedish
def translate_color(color):
    return color_translation.get(color, color)

# Function to translate color from English to Swedish
def translate_color(color):
    return color_translation.get(color, color)

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

# Function to load EANs from a CSV file
def load_eans_from_csv(filename):
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            ean_list = [row for row in reader if row['EAN'].strip()]  # Remove rows without EAN
        return ean_list
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

# Function to extract size information from product or offer name
def extract_size_from_name(name, expected_size):
    # Find any numbers followed by optional whitespace and metric indicators (cm, mm, etc.)
    match = re.search(rf"{expected_size}\s*(cm|mm|CM|MM|Ø|ø)", name, re.IGNORECASE)
    return match.group(0) if match else None

# Function to extract color from the product name
def extract_color_from_name(name):
    for color in swedish_colors:
        if color.lower() in name.lower():
            return color
    for eng_color, swe_color in color_translation.items():
        if eng_color.lower() in name.lower():
            return swe_color
    return "N/A"

# Main logic to search for each EAN and save details to a CSV
def main():
    input_filename = "ean_list.csv"  # Input CSV file containing EANs and other information
    output_filename = "ean_offers_with_details.csv"  # Output file for results
    delay_between_requests = 2  # Delay in seconds between requests

    # Load EANs from the input CSV file
    ean_list = load_eans_from_csv(input_filename)

    # Prepare the CSV file for writing results
    with open(output_filename, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "EAN", "Color", "Size", "Purchase Price", "Recommended Price",
            "ProductID", "Price", "StoreName", "Featured", "P Color", "P Size"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Process each EAN
        for row in ean_list:
            ean = row['EAN']
            color = row.get('Color', '').strip()
            size = row.get('Size', '').strip()
            purchase_price = row.get('Purchase Price', '')
            recommended_price = row.get('Recommended Price', '')

            # Determine final color based on input and translation
            if color:
                translated_color = translate_color(color)
                if translated_color not in swedish_colors and color not in color_translation.values():
                    # Attempt to find basic colors in the product name if color is unknown
                    translated_color = "N/A"
                color = translated_color

            print(f"\nSearching for EAN: {ean}")
            products = search_product_by_ean(ean)

            if products:
                for product in products:
                    product_name = product.get('name', '')
                    size_extracted = extract_size_from_name(product_name, size) if size else 'N/A'
                    p_color = extract_color_from_name(product_name)

                    # Handle Product details
                    if 'id' in product:  # Check if it's a Product
                        product_id = product['id']
                        print(f"Product Found: ID: {product_id}, Name: {product_name}, Extracted Size: {size_extracted}, Extracted Color: {p_color}")
                        writer.writerow({
                            "EAN": ean,
                            "Color": color,
                            "Size": size_extracted if size_extracted != 'N/A' else size,
                            "Purchase Price": purchase_price,
                            "Recommended Price": recommended_price,
                            "ProductID": product_id,
                            "Price": "N/A",
                            "StoreName": "N/A",
                            "Featured": "N/A",
                            "P Color": p_color,
                            "P Size": size_extracted
                        })

                    # Handle Offer details
                    if 'offerId' in product:  # Check if it's an Offer
                        store_name = product['store']['name']
                        price = product['offerPrice'].get('regular', 'N/A')
                        offer_id = product['offerId']
                        featured_status = "Yes" if product['store'].get('featured') else "No"
                        p_color = extract_color_from_name(product_name)
                        print(f"Offer Found: Store: {store_name}, Price: {price}, Offer ID: {offer_id}, Extracted Size: {size_extracted}, Extracted Color: {p_color}")
                        writer.writerow({
                            "EAN": ean,
                            "Color": color,
                            "Size": size_extracted,
                            "Purchase Price": purchase_price,
                            "Recommended Price": recommended_price,
                            "ProductID": "N/A",
                            "Price": price,
                            "StoreName": store_name,
                            "Featured": featured_status,
                            "P Color": p_color,
                            "P Size": size_extracted
                        })
            else:
                print(f"No products or offers found for EAN: {ean}")
                writer.writerow({
                    "EAN": ean,
                    "Color": color,
                    "Size": size,
                    "Purchase Price": purchase_price,
                    "Recommended Price": recommended_price,
                    "ProductID": "N/A",
                    "Price": "N/A",
                    "StoreName": "No Store Found",
                    "Featured": "",
                    "P Color": "",
                    "P Size": ""
                })

            # Introduce a delay between requests
            time.sleep(delay_between_requests)

    print(f"\nResults have been saved to {output_filename}")

if __name__ == "__main__":
    main()
