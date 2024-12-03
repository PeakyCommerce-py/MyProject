import requests
from bs4 import BeautifulSoup
import json
import csv
import re

# Cookies and headers for the Swedish session
cookies = {
    "amcookie_policy_restriction": "denied",
    "aw_popup_viewed_page": "[%22bbc9ba7666d7d88096971df7c13e31ac04c3066b8905a88c777a0e81916da2eb%22%2C%2249dbfcfcb53b336e2719463f32c08bfe8b9c930fafc270f194d6c9ba91578288%22]",
    "form_key": "l9cMINqASD3VdaSU",
    "PHPSESSID": "djmfnpb9cb4p5qikf93ljk097e",
    "_ALGOLIA_MAGENTO_AUTH": "aa-Y3VzdG9tZXItMDc0YWIwMzA0MjlkMWI1NTE0NmIyNDFjZjgxYjA3NDFhYTc2Y",
    "lvc-path-key": "1-2-75",
    "mage-cache-sessid": "true",
    "mage-cache-storage": "{}",
    "mage-cache-storage-section-invalidation": "{}",
    "mage-messages": "",
    "private_content_version": "f247af8ddb994aad8d1a0f305f1ce5f3",
    "product_data_storage": "{}",
    "recently_compared_product": "{}",
    "recently_compared_product_previous": "{}",
    "recently_viewed_product": "{}",
    "recently_viewed_product_previous": "{}",
    "section_data_ids": "{%22customer%22:1732541551%2C%22compare-products%22:1732541551%2C%22last-ordered-items%22:1732541551%2C%22cart%22:1732639610%2C%22directory-data%22:1732541551%2C%22captcha%22:1732541551%2C%22instant-purchase%22:1732541551%2C%22loggedAsCustomer%22:1732541551%2C%22persistent%22:1732639610%2C%22review%22:1732541551%2C%22wishlist%22:1732541551%2C%22ammessages%22:1732541551%2C%22recently_viewed_product%22:1732541551%2C%22recently_compared_product%22:1732541551%2C%22product_data_storage%22:1732541551%2C%22paypal-billing-agreement%22:1732541551}",
    "X-Magento-Vary": "63d48e8f09734a959877da340b848b952253d9a1ac543c36645be1d1f7747b38",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "sv-SE,sv;q=0.9,en;q=0.8",
}

config = {
    'brand': '.product.attribute.martinex-brand-attribute a',
    'name': 'h1.page-title span.base',
    'price': '.price-container .price',
    'description': '#long-desc',
    'meta_title': 'meta[name="title"]',
    'meta_description': 'meta[name="description"]',
    'breadcrumbs': '.breadcrumbs a',
    'stock_status': '.stock span',  # Lagerstatus
    'sku': '.product.attribute.sku span.value',  # Artikelnummer
}

base_url = "https://extranet.martinex.se/hemma"

def scrape_categories(base_url):
    """Scrape category links from the main 'Hemma' page."""
    response = requests.get(base_url, headers=headers, cookies=cookies, timeout=10)
    if response.status_code != 200:
        print(f"Failed to load categories. Status: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    categories = soup.select("li.category-item a")

    category_links = []
    for category in categories:
        category_name = category.text.strip()
        category_url = category["href"]

        # Only include links under the 'Hemma' category
        if category_url.startswith("https://extranet.martinex.se/hemma"):
            print(f"Category: {category_name} - {category_url}")
            category_links.append(category_url)

    # Save filtered category links to a file
    with open("categories.txt", "w", encoding="utf-8") as f:
        for link in category_links:
            f.write(link + "\n")

    return category_links


def scrape_product_links(category_url):
    """Scrape product links from a category page."""
    response = requests.get(category_url, headers=headers, cookies=cookies, timeout=10)
    if response.status_code != 200:
        print(f"Failed to load category: {category_url}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    products = soup.select(".product-item .product-item-link")

    links = [product["href"] for product in products]
    print(f"Found {len(links)} products in category: {category_url}")
    return links

def scrape_all_product_links(category_links):
    """Scrape all product links from multiple categories."""
    all_product_links = []
    for category_url in category_links:
        product_links = scrape_product_links(category_url)
        all_product_links.extend(product_links)

    # Save product links to a file
    with open("product_links.txt", "w", encoding="utf-8") as f:
        for link in all_product_links:
            f.write(link + "\n")

    return all_product_links


def scrape_product_details(product_url):
    """Scrape product details."""
    response = requests.get(product_url, headers=headers, cookies=cookies, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_data = {}

    # Brand
    brand = soup.select_one(config['brand'])
    product_data['Brand'] = brand.text.strip() if brand else ''

    # Name
    name = soup.select_one(config['name'])
    product_data['Name'] = name.text.strip() if name else ''

    # Price
    price = soup.select_one(config['price'])
    product_data['Price'] = price.text.strip() if price else ''

    # Description
    description = soup.select_one(config['description'])
    if description:
        product_data['Description'] = description.get_text(strip=True)
    else:
        product_data['Description'] = ''

    # Meta Title and Meta Description
    meta_title = soup.select_one(config['meta_title'])
    meta_description = soup.select_one(config['meta_description'])
    product_data['Meta Title'] = meta_title["content"] if meta_title else ''
    product_data['Meta Description'] = meta_description["content"] if meta_description else ''

    # Breadcrumbs (Over Category and Subcategory)
    breadcrumbs = soup.select(config['breadcrumbs'])
    if breadcrumbs and len(breadcrumbs) > 1:
        product_data['Over Category'] = breadcrumbs[-2].text.strip()
        product_data['Subcategory'] = breadcrumbs[-1].text.strip()
    else:
        product_data['Over Category'] = ''
        product_data['Subcategory'] = ''

    # Stock Status
    stock_status = soup.select_one(config['stock_status'])
    product_data['Stock Status'] = stock_status.text.strip() if stock_status else 'Unknown'

    # SKU (Artikelnummer)
    sku = soup.select_one(config['sku'])
    product_data['SKU'] = sku.text.strip() if sku else ''

    # Product ID (Huvud-ID)
    product_id = soup.select_one('[data-product-id]')
    product_data['Product ID'] = product_id['data-product-id'] if product_id else ''

    # Images
    images = []
    scripts = soup.find_all('script', type='text/x-magento-init')
    for script in scripts:
        if script.string and 'mage/gallery/gallery' in script.string:
            try:
                json_data = json.loads(script.string)
                gallery = json_data.get('[data-gallery-role=gallery-placeholder]', {}).get('mage/gallery/gallery', {})
                for img in gallery.get('data', []):
                    images.append(img.get('full', ''))
            except (json.JSONDecodeError, KeyError):
                continue
    product_data['Images'] = ', '.join(images)

    return product_data


def scrape_products_from_links(input_file, output_file):
    """Scrape product details and export to CSV."""
    with open(input_file, 'r', encoding='utf-8') as f:
        product_links = [line.strip() for line in f.readlines() if line.strip()]

        # Prepare for dynamic fieldnames
    fieldnames = set(['Brand', 'Name', 'Price', 'Description'])  # Predefined fields
    all_data = []

    for link in product_links:
        print(f"Scraping: {link}")
        try:
            product_data = scrape_product_details(link)
            all_data.append(product_data)
        except Exception as e:
            print(f"Error scraping {link}: {e}")

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_data)

    def main():
        # Steg 1: Skrapa kategorilänkar
        print("Scraping categories...")
        category_links = scrape_categories(base_url)

        if not category_links:
            print("No categories found. Exiting...")
            return

        # Steg 2: Skrapa produktlänkar från kategorier
        print("Scraping product links...")
        product_links = scrape_all_product_links(category_links)

        if not product_links:
            print("No product links found. Exiting...")
            return

        # Steg 3: Skrapa produktdetaljer och exportera till CSV
        print("Scraping product details...")
        scrape_products_from_links("product_links.txt", "products_output.csv")
        print("Scraping complete. Results saved to 'products_output.csv'.")

    if __name__ == "__main__":
        main()