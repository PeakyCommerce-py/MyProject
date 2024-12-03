import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL for search
SEARCH_URL = "https://www.annavonlipa.com/search/?string="

# Headers for the requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Function to generate URL-friendly product names
def format_product_name(name):
    return name.replace(" ", "-")

# Function to search for a product by SKU or product name
def search_product(query):
    try:
        response = requests.get(SEARCH_URL + query, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the product class
        product_div = soup.find("div", class_="product")
        if not product_div:
            print(f"No product found for query: {query}")
            return None, None, "Unknown"

        # Extract the product link
        product_link = product_div.find("a", class_="name")["href"]

        # Confirm the SKU matches (if SKU search was used)
        sku_span = product_div.find("span", {"data-micro": "sku"})
        sku = sku_span.get_text(strip=True) if sku_span else "N/A"
        stock_status = soup.select_one("div.availability span").get_text(strip=True) if soup.select_one("div.availability span") else "Unknown"

        print(f"Product link found: {product_link}, SKU: {sku}, Stock Status: {stock_status}")
        return "https://www.annavonlipa.com" + product_link, sku, stock_status
    except Exception as e:
        print(f"Error searching for query {query}: {e}")
        return None, None, "Unknown"

# Function to scrape images from the product page
def scrape_images_from_product_page(product_url):
    try:
        response = requests.get(product_url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract orig image first
        images = []
        orig_image = soup.select_one("a.p-main-image.cloud-zoom")
        if orig_image and "data-href" in orig_image.attrs:
            images.append(orig_image["data-href"])
            print(f"Scraped orig image: {orig_image['data-href']}")

        # Extract other images with "/big/"
        big_images = soup.select("div.p-thumbnails-inner a")
        for img in big_images:
            href = img.get("href", "")
            if "/big/" in href:
                images.append(href)
                print(f"Scraped big image: {href}")

        # Check if all images were scraped
        if images:
            print(f"All images scraped for product page: {product_url}")
        else:
            print(f"No images found for product page: {product_url}")

        # Format images with commas
        return ",".join(images)
    except Exception as e:
        print(f"Error scraping images from {product_url}: {e}")
        return "Error"

# Main function to process SKUs and generate output
def main():
    # Load SKUs from supplier data
    supplier_file = "supplier_file.csv"  # Replace with your file path
    supplier_data = pd.read_csv(supplier_file)

    results = []
    for index, row in supplier_data.iterrows():
        sku = row["SUPPLIER PRODUCT NUMBER"]
        product_name = row["SUPPLIER PRODUCT NAME"]
        print(f"\nSearching for SKU: {sku}")

        # Search for the product by SKU
        product_url, matched_sku, stock_status = search_product(sku)
        if not product_url:
            # If SKU search fails, search by product name
            print(f"SKU search failed. Trying with product name: {product_name}")
            formatted_name = format_product_name(product_name)
            product_url, matched_sku, stock_status = search_product(formatted_name)

        if product_url:
            print(f"Product page found: {product_url}, Stock Status: {stock_status}")

            # Scrape images from the product page
            images = scrape_images_from_product_page(product_url)
            results.append({"SKU": matched_sku, "IMG URL": images, "Stock Status": stock_status})
        else:
            print(f"No product found for SKU or name: {sku}")
            results.append({"SKU": sku, "IMG URL": "No Product", "Stock Status": "No Product"})

    # Save results to a CSV file
    output_file = "sku_with_images_and_stock.csv"
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"\nOutput saved to {output_file}")

# Run the script
if __name__ == "__main__":
    main()  