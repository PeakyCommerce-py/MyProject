import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_total_articles(brand_name):
    """
    Navigates to the brand URL and returns the total number of articles found.
    """
    brand_url = f"https://www.azdesign.se/sv/trademarks/{brand_name}"
    try:
        driver.get(brand_url)
        print(f"Opened URL: {brand_url}")

        # Wait for the element containing the article count to be visible
        article_count_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.totalArticles"))
        )
        article_count_text = article_count_element.text.strip()
        print(f"Article count text: {article_count_text}")

        # Extract the total number of articles
        total_count = int(article_count_text.split()[0].strip())
        return total_count
    except Exception as e:
        print(f"Error extracting article count from {brand_url}: {e}")
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
    df = pd.DataFrame(results, columns=["Brand Name", "Total Articles"])
    df.to_excel(output_file, index=False)

# Define file paths
brands_file = 'brands.txt'
output_file = 'brand_articles.xlsx'

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

# Extract article counts for each brand
results = []
for brand in brands:
    print(f"Processing brand: {brand}")
    total_articles = get_total_articles(brand)
    if total_articles != "Error":
        results.append((brand, total_articles))

# Close the driver
driver.quit()

# Save the results to an Excel file
save_results_to_excel(results, output_file)

print(f"Data saved to {output_file}")
