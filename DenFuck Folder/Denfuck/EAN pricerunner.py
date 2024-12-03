import requests
import csv
import time
import random
import re

# URLs for API endpoints
search_url = "https://www.pricerunner.se/se/api/search-compare-gateway/public/search/v5/SE?q={EAN}"
product_detail_url = "https://www.pricerunner.se/se/api/search-compare-gateway/public/product-detail/v0/offers/SE/{ID}?af_ORIGIN=NATIONAL&af_ITEM_CONDITION=NEW,UNKNOWN&sortByPreset=PRICE"

# Headers for requests
headers = {
    "accept": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
}

# Basic colors in Swedish and English
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


def detect_color_from_name(product_name):
    """Detect color from product name using basic colors and translate to Swedish if necessary."""
    for color in swedish_colors.union(color_translation.keys()):
        if re.search(rf"\b{color.lower()}\b", product_name.lower()):
            return color_translation.get(color, color)  # Translate to Swedish if in English
    return "Not Sure"

def fetch_product_id(ean):
    """Fetch product ID from EAN."""
    response = requests.get(search_url.format(EAN=ean), headers=headers)
    if response.status_code == 200:
        data = response.json()
        products = data.get("products", [])
        if products:
            return products[0]["id"]  # Return the first product ID found
    else:
        print(f"Failed to retrieve product ID for EAN: {ean}. Status code: {response.status_code}")
    return None

def fetch_price_and_merchant_info(product_id):
    """Fetch unique offers (price, merchant, color, offer ID) for a given product ID."""
    url = product_detail_url.format(ID=product_id)
    response = requests.get(url, headers=headers)
    offers_list = []

    if response.status_code == 200:
        data = response.json()
        offers = data.get("offers", [])
        if offers:
            for offer in offers:
                # Check if the offer is available and in stock
                if offer.get("availability") == "AVAILABLE" and offer.get("stockStatus") == "IN_STOCK":
                    # Extract price
                    price = float(offer["price"]["amount"])
                    if price.is_integer():
                        price = int(price)

                    # Extract merchant name and offer ID
                    merchant_id = str(offer["merchantId"])
                    merchant_name = data["merchants"].get(merchant_id, {}).get("name", "Unknown Merchant")
                    offer_id = offer.get("id", "No Offer ID")  # Retrieve the unique offer ID

                    # Primary color filtering: Check in `attributeLabels`
                    color = None
                    for label in offer.get("labels", {}).get("attributeLabels", []):
                        if label["name"].lower() == "färg" and label["value"] in swedish_colors:
                            color = label["value"]
                            break

                    # Secondary color filtering: Check in product `name` if not found in `attributeLabels`
                    if not color:
                        color = detect_color_from_name(offer["name"])

                    # Append the offer with price, merchant name, identified color, and offer ID
                    offers_list.append({
                        "price": price,
                        "merchantName": merchant_name,
                        "color": color,
                        "offer_id": offer_id  # Include offer ID for uniqueness
                    })
    else:
        print(f"Failed to retrieve details for Product ID {product_id}. Status code: {response.status_code}")

    return offers_list

def main():
    input_filename = "BloomingVilleMiniMarginsInputs.csv"
    output_filename = "Gustavbergputmargin.csv"

    with open(input_filename, mode="r", encoding="utf-8") as infile, open(output_filename, mode="w", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["BrandName", "Sell Price", "Color", "Offer ID"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            ean = row["EAN"]
            print(f"\nFetching offers for EAN: {ean}")
            product_id = fetch_product_id(ean)

            if product_id:
                offers = fetch_price_and_merchant_info(product_id)
                if offers:
                    for offer in offers:
                        # Update row with details for each unique offer
                        row.update({
                            "BrandName": offer["merchantName"],
                            "Sell Price": offer["price"],
                            "Color": offer["color"],
                            "Offer ID": offer["offer_id"]  # Add offer ID to output row
                        })
                        writer.writerow(row)
                else:
                    # Case where no offers are found for the product ID
                    row.update({
                        "BrandName": "No Product Found",
                        "Sell Price": "",
                        "Color": "Not Sure",
                        "Offer ID": "No Offer ID"  # Indicate no offer ID available
                    })
                    writer.writerow(row)
            else:
                # Case where no product ID is found for the EAN
                row.update({
                    "BrandName": "No Product Found",
                    "Sell Price": "",
                    "Color": "Not Sure",
                    "Offer ID": "No Offer ID"  # Indicate no offer ID available
                })
                writer.writerow(row)

            delay = random.randint(1, 3)
            print(f"Sleeping for {delay} seconds to avoid detection as a bot.")
            time.sleep(delay)

if __name__ == "__main__":
    main()
