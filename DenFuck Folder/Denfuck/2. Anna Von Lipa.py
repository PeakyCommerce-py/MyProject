import requests
from bs4 import BeautifulSoup

# Base URL for the website
BASE_URL = "https://www.annavonlipa.com"

# Headers to mimic a browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}


# Function to extract all links containing "https"
def extract_links(file_path):
    links = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if "https" in line:  # Check for "https" in the line
                link = line.split()[-1]  # Extract the last part of the line (URL)
                links.append(link)
    return links


# Function to scrape product links from a category page
def scrape_products_from_category(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Raise error for bad status codes
        soup = BeautifulSoup(response.content, "html.parser")

        # Find product links
        product_links = []
        products = soup.find_all("div", class_="product")
        for product in products:
            product_anchor = product.find("a", href=True)
            if product_anchor:
                product_url = product_anchor["href"]
                # Ensure full URL
                if not product_url.startswith("http"):
                    product_url = f"https://www.annavonlipa.com{product_url}"
                product_links.append(product_url)

        return product_links
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []


# Save product links to a file
def save_to_file(data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        for item in data:
            file.write(item + "\n")
    print(f"Saved to {file_path}")


# Main function
def main():
    input_file = "C:\\Users\\Dejan\\PycharmProjects\\Denfuck\\category_output.txt"
    output_file = "C:\\Users\\Dejan\\PycharmProjects\\Denfuck\\product_links.txt"

    # Extract subcategory links
    subcategory_links = extract_links(input_file)
    print(f"Found {len(subcategory_links)} subcategories to scrape.")

    # Scrape products
    all_product_links = []
    for subcategory in subcategory_links:
        print(f"Scraping: {subcategory}")
        product_links = scrape_products_from_category(subcategory)
        all_product_links.extend(product_links)

    # Save product links
    save_to_file(all_product_links, output_file)


# Run script
if __name__ == "__main__":
    main()