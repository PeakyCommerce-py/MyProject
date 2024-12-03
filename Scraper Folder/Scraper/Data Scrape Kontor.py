import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote, unquote
import re

def sanitize_filename(filename):
    """
    Sanitize the filename by removing or replacing invalid characters.
    """
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def get_categories_and_counts(brand_name):
    """
    Navigates to the brand URL and returns the categories and their product counts.
    """
    search_url = f"https://www.lomax.se/varumarken/{quote(brand_name)}"
    categories_and_counts = []
    for attempt in range(2):  # Try up to 2 times
        try:
            driver.get(search_url)

            try:
                category_elements = WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.w-100.text-break.two-line"))
                )
                for element in category_elements:
                    category_text = element.text.strip()
                    if category_text:
                        category = category_text.split('\n')[0].strip()
                        count = int(element.find_element(By.CSS_SELECTOR, "small.text-muted").text.strip('()'))
                        categories_and_counts.append((category, count))
                return categories_and_counts
            except Exception as e:
                print(f"Error extracting categories from {search_url} on attempt {attempt + 1}: {e}")
                # Save the page source for debugging
                with open(f"error_page_{sanitize_filename(brand_name)}_attempt_{attempt + 1}.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
        except Exception as e:
            print(f"An error occurred while processing {search_url} on attempt {attempt + 1}: {e}")
            # Save the page source for debugging
            with open(f"error_page_{sanitize_filename(brand_name)}_attempt_{attempt + 1}.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
    return "Error"

def read_brands_from_excel(file_name):
    """
    Reads the brands from the specified Excel file.
    """
    df = pd.read_excel(file_name)
    return df['Links'].tolist()

# Initialize the Chrome driver with options to make it faster
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Uncomment to run in headless mode for faster performance
options.add_argument('--disable-gpu')  # Disable GPU usage
options.add_argument('--no-sandbox')  # Bypass OS security model
options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

driver = webdriver.Chrome(options=options)

# Open the Lomax search page and wait for manual actions
driver.get('https://www.lomax.se/varumarken')
print("Please close any cookies pop-ups within 5 seconds...")
WebDriverWait(driver, 8).until_not(EC.presence_of_element_located((By.ID, 'cookie-notification')))  # Wait for cookies pop-up to disappear

# Read brands from the Excel file
brands = read_brands_from_excel('execution.xlsx')

all_categories_counts = []

# Process each brand and get categories and their counts
for brand_url in brands:
    # Extract brand name from URL
    brand_name = unquote(brand_url.split('/')[-2])
    categories_and_counts = get_categories_and_counts(brand_name)
    all_categories_counts.append((brand_name, categories_and_counts))

# Close the driver
driver.quit()

# Save the results to a text file
with open('categories_counts.txt', 'w', encoding='utf-8') as file:
    for brand_name, categories_and_counts in all_categories_counts:
        file.write(f"{brand_name}:\n")
        if categories_and_counts == "Error":
            file.write("  Error\n")
        else:
            for category, count in categories_and_counts:
                file.write(f"  {category}: {count}\n")

print("Data saved to categories_counts.txt")
