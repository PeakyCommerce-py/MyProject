import json
import csv
from bs4 import BeautifulSoup

def scrape_and_categorize_products(base_url, input_file):
    # Read the raw data from the file
    with open(input_file, 'r', encoding='utf-8') as file:
        json_str = file.read()

    try:
        data = json.loads(json_str)
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return

    # Extract the category name from the data
    category_name = 'UnknownCategory'
    filters = data.get('filters', [])
    for filter_item in filters:
        if filter_item.get('param') == 'SubCategory':
            selected_options = filter_item.get('selectedOptions', [])
            if selected_options:
                category_name = selected_options[0].get('value', 'UnknownCategory')
            break

    # Normalize the category name for the file name
    category_name_safe = category_name.replace(' ', '_').replace('/', '_')

    total_products = data.get('moduleSettings', {}).get('productCount', None)
    total_pages = data.get('moduleSettings', {}).get('pageCount', None)
    print(f"Category: {category_name}")
    print(f"Expected total products: {total_products}, total pages: {total_pages}")

    # Ensure total_pages is a valid number
    if total_pages is None or total_pages <= 0:
        print(f"Invalid total_pages value: {total_pages}. Exiting...")
        return

    # Initialize a dictionary to store products per brand
    brands = {}

    # Extract products from the data
    page_products = 0
    for product in data.get('products', []):
        product_id = product.get('id')

        # Parse listItemHtml to extract the product link
        soup = BeautifulSoup(product['listItemHtml'], 'html.parser')
        product_anchor = soup.find('a', class_="e-productlist-item-image-wrapper")
        if product_anchor and product_anchor.get('href'):
            product_link = base_url + product_anchor.get('href')

            # Extract brand information from h4 tag with class 'float-left'
            brand_element = soup.find('h4', class_='float-left')
            if brand_element:
                brand_name = brand_element.get_text(strip=True)
            else:
                brand_name = 'UNKNOWN'

            # Normalize the brand name to uppercase
            brand_name_upper = brand_name.upper()

            # Debug print to check the extracted brand name
            print(f"Product ID {product_id}: Brand - {brand_name_upper}")

            # Add the product link to the appropriate brand list
            if brand_name_upper not in brands:
                brands[brand_name_upper] = []
            brands[brand_name_upper].append(product_link)

            page_products += 1
        else:
            print(f"Skipping product with ID: {product_id} (No href found)")

    print(f"Scraped {page_products} products.")

    # Prepare data for CSV output
    max_length = max(len(links) for links in brands.values()) if brands else 0
    csv_rows = []

    # Create headers (horizontal)
    headers = list(brands.keys())
    csv_rows.append(headers)

    # Build rows
    for i in range(max_length):
        row = []
        for brand in headers:
            try:
                row.append(brands[brand][i])
            except IndexError:
                row.append('')  # If there are no more links for this brand
        csv_rows.append(row)

    # Create the output file name based on the category
    output_file = f"{category_name_safe}_Links.csv"

    # Write the results to a CSV file
    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_rows)

    print(f"\nCategorized product links saved to '{output_file}'.")

# Configuration
base_url = "https://www.bloomingville.com"
input_file = "article_numbers.txt"

# Run the script
scrape_and_categorize_products(base_url, input_file)
