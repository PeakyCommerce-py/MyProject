import requests
from bs4 import BeautifulSoup
import csv

# Headers to mimic a browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}


# Function to scrape product details from a URL
def scrape_product_details(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract product name
        name = soup.select_one("div.p-detail-inner-header h1")
        name = name.get_text(strip=True) if name else "N/A"

        # Extract availability and stock
        availability_block = soup.select_one("div.p-basic-info-block")
        availability_label = availability_block.select_one("span.availability-label")
        availability_text = availability_label.get_text(strip=True) if availability_label else "N/A"
        stock = availability_block.select_one("span.availability-amount")
        stock = stock.get_text(strip=True) if stock else "N/A"
        availability = f"{availability_text} {stock}"

        # Extract SKU
        sku_block = availability_block.select_one("span.p-code span:nth-child(2)")
        sku = sku_block.get_text(strip=True) if sku_block else "N/A"

        # Extract price
        price_block = soup.find("script", text=lambda t: t and '"items":' in t)
        price = "N/A"
        if price_block:
            price_data = price_block.string.strip()
            start = price_data.find('"price":') + len('"price":')
            end = price_data.find(",", start)
            price = price_data[start:end].strip()

        # Extract description
        description_block = soup.select_one("div.basic-description div.mt-3 p")
        description = description_block.decode_contents() if description_block else "N/A"

        # Extract details
        details_block = soup.select("div.p-short-description p")
        details = []
        for detail in details_block:
            text = detail.get_text(strip=True)
            if text:
                key_value = text.split(":")
                if len(key_value) == 2:
                    key, value = key_value
                    details.append(f"Produktinformation_{key.strip()}_{value.strip()}")
        details = ",".join(details)

        # Extract images
        image_blocks = soup.select("div.p-image-wrapper a")
        orig_image = None
        big_images = []
        for image in image_blocks:
            href = image.get("href")
            if "/orig/" in href:
                orig_image = href
            elif "/big/" in href:
                big_images.append(href)
        images = [orig_image] + big_images if orig_image else big_images
        images = ",".join(images)

        # Return scraped data
        return {
            "Name": name,
            "Availability": availability,
            "Artikel Nummer": sku,
            "Price €": price,
            "Details": details,
            "Description": description,
            "Images": images
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return {
            "Name": "Error",
            "Availability": "Error",
            "Artikel Nummer": "Error",
            "Price €": "Error",
            "Details": "Error",
            "Description": "Error",
            "Images": "Error"
        }


# Main function to scrape all product links and save to CSV
def main():
    input_file = "C:\\Users\\Dejan\\PycharmProjects\\Denfuck\\product_links.txt"
    output_file = "C:\\Users\\Dejan\\PycharmProjects\\Denfuck\\product_details.csv"

    # Read product links from file
    with open(input_file, "r", encoding="utf-8") as file:
        product_links = [line.strip() for line in file if line.strip()]

    # Scrape product details
    product_data = []
    for idx, link in enumerate(product_links):
        print(f"Scraping {idx + 1}/{len(product_links)}: {link}")
        data = scrape_product_details(link)
        product_data.append(data)

    # Save data to CSV
    fieldnames = ["Name", "Availability", "Artikel Nummer", "Price €", "Details", "Description", "Images"]
    with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(product_data)

    print(f"Scraped data saved to {output_file}")


# Run the script
if __name__ == "__main__":
    main()
