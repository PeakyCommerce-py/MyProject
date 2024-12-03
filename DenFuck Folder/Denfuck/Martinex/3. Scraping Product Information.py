import requests
from bs4 import BeautifulSoup
import json
import csv
import re

# Headers and cookies
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "sv-SE,sv;q=0.9,en;q=0.8"
}

cookies = {
    "amcookie_policy_restriction": "denied",
    "aw_popup_viewed_page": "[%22bbc9ba7666d7d88096971df7c13e31ac04c3066b8905a88c777a0e81916da2eb%22%2C%2249dbfcfcb53b336e2719463f32c08bfe8b9c930fafc270f194d6c9ba91578288%22]",
    "form_key": "l9cMINqASD3VdaSU",
    "PHPSESSID": "djmfnpb9cb4p5qikf93ljk097e"
    # Add the remaining cookies
}

# Configuration for selectors
config = {
    'brand': '.product.attribute.martinex-brand-attribute a',
    'name': 'h1.page-title span.base',
    'price': '.price-container .price',
    'description': '#long-desc',
    'meta_title': 'meta[name="title"]',
    'meta_description': 'meta[name="description"]',
    'related_products': '[data-product-id]',
    'breadcrumbs': '.breadcrumbs a'
}

# Scraping product details
def scrape_product_details(product_url):
    response = requests.get(product_url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_data = {}

    # Brand
    brand = soup.select_one('.product.attribute.martinex-brand-attribute a')
    product_data['Brand'] = brand.text.strip() if brand else 'Unknown'

    # Name
    name = soup.select_one('h1.page-title span.base')
    product_data['Name'] = name.text.strip() if name else 'Unknown'

    # Availability
    availability = soup.select_one('.stock.available span')
    if availability and "Omedelbart" in availability.text:
        product_data['Availability'] = "Finns Lager"
    else:
        product_data['Availability'] = "Ej Lager"

    # Description
    description = soup.select_one('#long-desc')
    if description:
        description_text = description.get_text(strip=True)  # Hämta endast text
        product_data['Description'] = f"<div>{description_text}</div>"  # Formatera som HTML
    else:
        product_data['Description'] = "<div>No Description Available</div>"

    # Meta Title
    meta_title = soup.select_one('meta[name="title"]')
    if meta_title and meta_title.get("content"):
        meta_title_text = meta_title["content"].replace("Martinex", "NordicDetails.se")
        product_data['Meta Title'] = meta_title_text
    else:
        product_data['Meta Title'] = "No Meta Title Available"

    # Meta Description
    meta_description = soup.select_one('meta[name="description"]')
    if meta_description and meta_description.get("content"):
        product_data['Meta Description'] = meta_description["content"]
    else:
        product_data['Meta Description'] = "No Meta Description Available"

    # Details table (Produktinformation)
    details_table = soup.select('table#product-attribute-specs-table tr')
    details = []
    for row in details_table:
        key = row.select_one('th')
        value = row.select_one('td')
        if key and value:
            key_text = key.get_text(strip=True).replace(" ", "_")
            value_text = value.get_text(strip=True)
            details.append(f"Produktinformation_{key_text}_{value_text}")
    product_data['Details'] = ",".join(details)

    # Breadcrumbs for Over Category and Subcategory
    breadcrumbs = soup.find_all("script", type="application/ld+json")
    for script in breadcrumbs:
        try:
            data = json.loads(script.string)
            if data.get("@type") == "BreadcrumbList":
                items = data.get("itemListElement", [])
                product_data['Over Category'] = items[2]["name"] if len(items) > 2 else "Unknown"
                product_data['Subcategory'] = items[3]["name"] if len(items) > 3 else "Unknown"
                break
        except (json.JSONDecodeError, KeyError):
            continue

    # Extract ID and Artikel Nummer (SKU) from embedded JSON in <script>
    scripts = soup.find_all('script')
    for script in scripts:
        if script.string and 'dataLayer.push' in script.string:  # Kontrollera om scriptet innehåller 'dataLayer.push'
            try:
                # Extrahera JSON-strukturen från dataLayer.push
                json_match = re.search(r'dataLayer.push\((\{.*?\})\);', script.string, re.DOTALL)
                if json_match:
                    raw_json = json_match.group(1)

                    # Sanera JSON-strukturen
                    sanitized_json = re.sub(r"'", '"', raw_json)  # Byt ut enkelcitat mot dubbelcitat
                    sanitized_json = re.sub(r"(?<=\w):", '":', sanitized_json)  # Lägg till dubbelcitat runt nycklar

                    # Ladda den sanerade JSON-strukturen
                    json_data = json.loads(sanitized_json)

                    # Hämta ID och SKU från JSON-strukturen
                    products = json_data.get("ecommerce", {}).get("detail", {}).get("products", [])
                    if products:
                        product = products[0]  # Första produkten i listan
                        product_data['Artikel Nummer'] = product.get("sku", "Unknown")
                        product_data['ID'] = product.get("id", "Unknown")
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error parsing JSON for ID and SKU: {e}")



    # Extract images from JSON
    scripts = soup.find_all('script', type='text/x-magento-init')
    images = []
    for script in scripts:
        if script.string and 'mage/gallery/gallery' in script.string:
            try:
                json_data = json.loads(script.string)
                gallery_data = json_data['[data-gallery-role=gallery-placeholder]']['mage/gallery/gallery']
                for image in gallery_data['data']:
                    images.append(image.get('full', ''))
            except (json.JSONDecodeError, KeyError):
                continue
    product_data['Images'] = ", ".join(images)

    # Extract Related Products by SKU
    related_product_skus = []
    related_products = soup.select('form[data-role="tocart-form"]')
    for related in related_products:
        product_sku = related.get('data-product-sku', None)
        if product_sku:
            related_product_skus.append(product_sku)
    product_data['Related IDs'] = ','.join(related_product_skus)  # Lägg till relaterade SKUs

    return product_data


# Function to scrape products from a list of links
def scrape_products_from_links(input_file, output_file):
    # Read product links from file
    with open(input_file, 'r', encoding='utf-8') as f:
        product_links = [line.strip() for line in f.readlines() if line.strip()]

    # Prepare for CSV output
    fieldnames = [
        'Brand', 'Name', 'Availability', 'Description', 'Details',
        'Over Category', 'Subcategory', 'ID', 'Related IDs','Images',
        'Meta Title', 'Meta Description', 'Artikel Nummer'
    ]

    all_data = []

    for link in product_links:
        print(f"Scraping: {link}")
        try:
            product_data = scrape_product_details(link)
            all_data.append(product_data)
        except Exception as e:
            print(f"Error scraping {link}: {e}")

    # Write results to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_data)


# Example Usage
if __name__ == "__main__":
    input_file = "../product_links.txt"  # List of product URLs
    output_file = "../products_output.csv"  # Output CSV file
    scrape_products_from_links(input_file, output_file)