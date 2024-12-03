import requests
import re
import json
from bs4 import BeautifulSoup

# Input and output file paths
input_file = "../Subcategories.txt"
output_file = "../ProductLinks.txt"

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

def fetch_product_links(category_url):
    """Fetch all product links from a given category URL."""
    try:
        response = requests.get(category_url, headers=headers, cookies=cookies, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch {category_url}. Status code: {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        product_links = []

        # Look for <a> tags with the class 'product-item-link'
        product_items = soup.find_all("a", class_="product-item-link")
        for item in product_items:
            href = item.get("href")
            if href:
                product_links.append(href.strip())

        return product_links
    except Exception as e:
        print(f"Error fetching products from {category_url}: {e}")
        return []


def process_subcategories(input_file, output_file):
    """Process all subcategory links and extract product links."""
    try:
        with open(input_file, "r", encoding="utf-8") as infile:
            subcategory_urls = [line.strip() for line in infile if line.strip()]

        all_product_links = []

        for index, url in enumerate(subcategory_urls):
            print(f"Processing ({index + 1}/{len(subcategory_urls)}): {url}")

            # Fetch product links from the URL
            product_links = fetch_product_links(url)

            if product_links:
                print(f"Found {len(product_links)} product links in {url}")
            else:
                print(f"No product links found in {url}")

            all_product_links.extend(product_links)

        # Save results to the output file
        with open(output_file, "w", encoding="utf-8") as outfile:
            for link in all_product_links:
                outfile.write(link + "\n")

        print(f"Extracted {len(all_product_links)} product links.")
        print(f"Product links saved to {output_file}.")
    except Exception as e:
        print(f"Error processing subcategories: {e}")


# Run the script
process_subcategories(input_file, output_file)