import requests
from bs4 import BeautifulSoup
import csv
import re
import time

BASE_URL = "https://royaldesign.se"
BRAND_URL = "https://royaldesign.se/varumarken/oyoy"
CSV_FILE = "oyoy_products.csv"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Safari/537.36"
}


def get_product_links(page_number=1):
    product_links = []
    response = requests.get(f"{BRAND_URL}?page={page_number}", headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        product_list_items = soup.select(".css-41ps9a a.css-3toq9l")
        for item in product_list_items:
            product_links.append(BASE_URL + item.get("href"))
    return product_links


def scrape_product_details(product_url):
    product_data = {}
    response = requests.get(product_url, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Product Name
        product_name = soup.select_one(
            '#react-root > div > section:nth-of-type(1) > div > div:nth-of-type(2) > div > h1')
        product_data['Product Name'] = product_name.get_text(strip=True) if product_name else None

        # Breadcrumbs
        breadcrumbs = soup.select_one("nav.css-1mky92p div.css-b3k873:last-child span")
        if breadcrumbs:
            product_data['Breadcrumbs'] = breadcrumbs.get_text(strip=True)

        # Brand Name
        brand_name = soup.select_one('[id="react-root"] h3')
        product_data['Brand Name'] = brand_name.get_text(strip=True) if brand_name else None

        # Brand Information
        brand_info = soup.select_one('span.css-1to9izb')
        product_data['Brand Information'] = brand_info.get_text(strip=True) if brand_info else None

        # Price
        price = soup.select_one('[id="react-root"] span.current-price')
        if price:
            # Remove any spaces to keep only the numeric price with "kr"
            cleaned_price = re.sub(r"\s", "", price.get_text(strip=True))
            product_data['Price'] = cleaned_price
        else:
            product_data['Price'] = None

        # Recommended Price
        rec_price = soup.select_one('span.css-xjqc32')
        if rec_price:
            # Remove "Rek. pris" and any spaces
            cleaned_rec_price = re.sub(r"Rek\. pris|\s", "", rec_price.get_text(strip=True))
            product_data['Recommended Price'] = cleaned_rec_price
        else:
            product_data['Recommended Price'] = None

        # Short Description
        short_desc = soup.select_one('div.css-ueu7xw')
        product_data['Short Description'] = short_desc.get_text(strip=True) if short_desc else None

        # Color of Product
        color = soup.select_one('p.css-1v4ngpm')
        product_data['Color'] = color.get_text(strip=True) if color else None

        # Function to select the 800-pixel version of the image from srcset, if available
        def get_800w_image(img_tag):
            srcset = img_tag.get('srcset')
            if srcset:
                # Look for 800w in srcset, return that URL
                sources = [s.strip() for s in srcset.split(',')]
                for source in sources:
                    if 'w=800' in source:
                        return source.split()[0]  # Return the URL for the 800w version
            return img_tag.get('src')  # Fallback to 'src' if no 800w found

        # Primary image
        picture = soup.select_one('div.css-rztiyz > img')
        product_data['Picture'] = get_800w_image(picture) if picture else None

        # Variant images
        variant_images = set()  # Use a set to avoid duplicates
        # Target the specific div where variant images are found
        variant_image_container = soup.select_one('div.css-52ryxc')  # Update this selector if it changes
        if variant_image_container:
            for img in variant_image_container.select('img'):
                img_url = get_800w_image(img)
                if img_url:
                    variant_images.add(img_url)  # Add to set to avoid duplicates

        # Join variant images as a comma-separated string for CSV storage
        product_data['Variant Images'] = ", ".join(variant_images) if variant_images else None

        # Description with HTML structure intact
        description = soup.select_one('span.css-em57a2 > div')
        product_data['Description'] = str(description) if description else None

        # Artikelnummer
        art = soup.select_one('li.css-y11wr6 > div.css-1sp3jtb > span.product-sku.css-lbcv1j')
        product_data['Art'] = art.get_text(strip=True) if art else None

        # Leverantörens Artikelnummer
        lev_art = None
        product_info_list = soup.find_all('li', class_='css-y11wr6')
        for item in product_info_list:
            label = item.select_one('div.css-ae1b0h')
            if label and "Lev. artikelnummer" in label.get_text(strip=True):
                lev_art_value = item.select_one('div.css-1sp3jtb span')
                if lev_art_value:
                    lev_art = lev_art_value.get_text(strip=True)
                break

        product_data['Lev.Art'] = lev_art if lev_art else None

        # Product Information (All <li> elements under the characteristics panel)
        product_info_list = soup.find_all(class_='css-y11wr6')
        properties = []
        for item in product_info_list:
            key = item.select_one('div.css-ae1b0h')
            value = item.select_one('div.css-1sp3jtb span') or item.select_one('div.css-1sp3jtb')
            if key and value:
                key_text = key.get_text(strip=True)
                value_text = value.get_text(strip=True)
                # Concatenate key and value in the format you prefer
                properties.append(f"Produktinformation_{key_text}_{value_text}")

        # Add the concatenated properties to the product data
        if properties:
            product_data['Properties'] = ",".join(properties)  # Join all key-value pairs as a single string

        # MetaDescription
        meta_description = soup.select_one('meta[name="description"]')
        product_data['MetaDescription'] = meta_description['content'] if meta_description else None

        # MetaTitle
        meta_title = soup.select_one('title')
        if meta_title:
            # Replace "RoyalDesign.se" with "NordicDetails.se" in the title
            title_content = meta_title.get_text(strip=True).replace("RoyalDesign.se", "NordicDetails.se")
            product_data['MetaTitle'] = title_content
        else:
            product_data['MetaTitle'] = None

        return product_data


def save_to_csv(products):
    fieldnames = [
        "Product Name",
        "Brand Name",
        "Breadcrumbs",
        "Art",
        "Lev.Art",
        "Price",
        "Recommended Price",
        "Short Description",
        "Description",
        "Color",
        "Picture",
        "Variant Images",
        "Properties",
        "Brand Information",
        "MetaTitle",
        "MetaDescription",
        "Website"
    ]

    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)


def main():
    all_products = []
    for page in range(1, 5):  # You can adjust the range to include more pages if needed
        product_links = get_product_links(page)
        for link in product_links:
            print(f"Scraping {link}")
            product_details = scrape_product_details(link)
            product_details['Website'] = link  # Save the actual product URL
            all_products.append(product_details)
    save_to_csv(all_products)
    print("Scraping completed and data saved to CSV.")



if __name__ == "__main__":
    main()