import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_total_products(brand_name):
    """
    Navigates to the brand URL and returns the total number of products found.
    """
    brand_url = f"https://www.swedoffice.se/varumarken/{brand_name}"
    try:
        driver.get(brand_url)
        print(f"Opened URL: {brand_url}")

        # Wait for the element containing the product count to be visible
        filter_select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "select.filterselect"))
        )
        options = filter_select_element.find_elements(By.CSS_SELECTOR, "option")

        total_count = 0
        for option in options:
            text = option.text.strip()
            if '(' in text and ')' in text:
                count = int(text.split('(')[-1].split(')')[0])
                total_count += count

        return total_count
    except Exception as e:
        print(f"Error extracting product count from {brand_url}: {e}")
        return "Error"


def read_brands_from_text(file_path):
    """
    Reads the brand names from a text file.
    """
    with open(file_path, 'r') as file:
        brands = [line.strip() for line in file]
    return brands


def save_results_to_excel(results, output_file):
    """
    Saves the search results to an Excel file.
    """
    df = pd.DataFrame(results, columns=["Brand Name", "Total Products"])
    df.to_excel(output_file, index=False)


# Define file paths
brands_file = 'brands.txt'
output_file = 'brand_products.xlsx'

# Read brands from the text file
brands = read_brands_from_text(brands_file)

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
for brand in brands:
    print(f"Processing brand: {brand}")
    total_products = get_total_products(brand)
    if total_products != "Error":
        results.append((brand, total_products))

# Close the driver
driver.quit()

# Save the results to an Excel file
save_results_to_excel(results, output_file)

print(f"Data saved to {output_file}")
