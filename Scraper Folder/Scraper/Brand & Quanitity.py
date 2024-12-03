import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def get_total_products(brand_url):
    """
    Navigates to the brand URL and returns the total number of products found.
    """
    driver.get(brand_url)
    print(f"Opened URL: {brand_url}")

    try:
        # Check for 'av' or 'under' in the text and extract the part after it
        if 'av' in load_more_text:
            parts = load_more_text.split('av')
        elif 'under' in load_more_text:
            parts = load_more_text.split('under')
        else:
            parts = []

        if len(parts) > 1:
            total_count_text = parts[1].strip()  # Get the part after 'av' or 'under'
            total_count = int(total_count_text.split()[0])  # Extract the first number after 'av' or 'under'
            print(f"Total product count from load more: {total_count}")
            return total_count
    except Exception as e:
        print(f"Load more element not found or not applicable: {e}")

    try:
        # Scenario 2: Check if there are product boxes for brands with 24 or fewer products
        product_listing_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-listing"))
        )
        product_boxes = product_listing_element.find_elements(By.CSS_SELECTOR, "product-box")
        total_count = len(product_boxes)
        print(f"Total product count from product boxes: {total_count}")
        return total_count
    except Exception as e:
        print(f"Error counting product boxes or no products found: {e}")
        return "No products"

def read_brands_from_text(file_path):
    """
    Reads the brand names and links from a text file.
    """
    brands = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():
                parts = line.strip().split('/')
                brand_name = parts[-1].replace('-', ' ').title()  # Extract brand name from URL and format it
                brands[brand_name] = line.strip()
    return brands

def save_results_to_excel(results, output_file):
    """
    Saves the search results to an Excel file.
    """
    df = pd.DataFrame(results, columns=["Brand Name", "Product Count"])
    df.to_excel(output_file, index=False)

# Define file paths
brands_file = 'urls.txt'
output_file = 'brand_products.xlsx'

# Read brands from the text file
brands = read_brands_from_text(brands_file)
print(f"Brands read from text file: {brands}")

# Initialize the Chrome driver
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')  # Disable GPU usage
options.add_argument('--no-sandbox')  # Bypass OS security model
options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

driver = webdriver.Chrome(options=options)

# Open a blank page and wait for manual actions (e.g., accepting cookies)
driver.get('https://www.google.com')
print("Please complete any manual actions within 5 seconds...")
time.sleep(5)

# Extract product counts for each brand
results = []
for brand, url in brands.items():
    print(f"Processing brand: {brand}")
    total_products = get_total_products(url)
    if total_products != "Error" and total_products != "No products":
        results.append((brand, total_products))
    else:
        print(f"Failed to process brand: {brand}")

# Close the driver
driver.quit()

# Save the results to an Excel file
save_results_to_excel(results, output_file)

print(f"Data saved to {output_file}")
