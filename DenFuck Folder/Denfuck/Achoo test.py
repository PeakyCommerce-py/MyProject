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

def detect_color_from_name(product_name, expected_color=None):
    """Detect color based on expected color or by checking against basic colors."""
    # Step 1: Check if the expected color is present in the product name
    if expected_color and re.search(rf"\b{re.escape(expected_color.lower())}\b", product_name.lower()):
        return expected_color  # Return expected color if found exactly in the name

    # Step 3: Fallback to checking against basic colors if no expected color found in name
    for color in swedish_colors.union(color_translation.keys()):
        if re.search(rf"\b{color.lower()}\b", product_name.lower()):
            return color_translation.get(color, color)  # Translate to Swedish if necessary
    return "Not Sure"

def fetch_price_and_merchant_info(product_id, expected_color=None):
    """Fetch unique offers (price, merchant, color, offer ID) for a given product ID, only if in stock and available."""
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
                    price = float(offer["price"]["amount"])
                    price = int(price) if price.is_integer() else price
                    merchant_name = data["merchants"].get(str(offer["merchantId"]), {}).get("name", "Unknown Merchant")
                    offer_id = offer.get("id", "No Offer ID")

                    # Step 1: Look for color in `attributeLabels`
                    color = None
                    for label in offer.get("labels", {}).get("attributeLabels", []):
                        if label["name"].lower() == "färg":
                            # Check if the color matches the expected color or use it as detected color
                            if expected_color is None or label["value"].lower() == expected_color.lower():
                                color = label["value"]
                                break

                    # Step 2: If no color match in `attributeLabels`, use detect_color_from_name to find in product name
                    if not color:
                        color = detect_color_from_name(offer["name"], expected_color)

                    # Step 4: If no color is detected, set color to "Not Sure"
                    if not color:
                        color = "Not Sure"

                    # Append the offer details to the list
                    offers_list.append({
                        "price": price,
                        "merchantName": merchant_name,
                        "color": color,
                        "offer_id": offer_id
                    })
    else:
        print(f"Failed to retrieve details for Product ID {product_id}. Status code: {response.status_code}")

    return offers_list

def main():
    input_filename = "BloomingVilleMarginsInputs.csv"
    output_filename = "BloomingVilleMarginsOutput.csv"

    with open(input_filename, mode="r", encoding="utf-8") as infile, open(output_filename, mode="w", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["BrandName", "Sell Price", "Color", "Offer ID"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            ean = row["EAN"]
            expected_color = row.get("Brand Color", None)  # Extract brand color from input file, if exists
            print(f"\nFetching offers for EAN: {ean} with expected color: {expected_color}")
            product_id = fetch_product_id(ean)

            if product_id:
                offers = fetch_price_and_merchant_info(product_id, expected_color)
                if offers:
                    for offer in offers:
                        row.update({
                            "BrandName": offer["merchantName"],
                            "Sell Price": offer["price"],
                            "Color": offer["color"],
                            "Offer ID": offer["offer_id"]
                        })
                        writer.writerow(row)
                else:
                    # Case where no offers are found for the product ID
                    row.update({
                        "BrandName": "No Product Found",
                        "Sell Price": "",
                        "Color": "Not Sure",
                        "Offer ID": "No Offer ID"
                    })
                    writer.writerow(row)
            else:
                # Case where no product ID is found for the EAN
                row.update({
                    "BrandName": "No Product Found",
                    "Sell Price": "",
                    "Color": "Not Sure",
                    "Offer ID": "No Offer ID"
                })
                writer.writerow(row)

            time.sleep(random.randint(1, 6))

if __name__ == "__main__":
    main()
