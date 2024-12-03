import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def search_brand_on_google(brand_domain):
    """
    Searches for the brand domain on Google and returns the first three links.
    """
    search_url = "https://www.google.com/"
    driver.get(search_url)

    try:
        # Accept cookies if prompted
        accept_cookies_button = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='I agree']"))
        )
        accept_cookies_button.click()
    except:
        pass  # If there's no cookies prompt, continue

    try:
        search_box = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.clear()
        search_box.send_keys(brand_domain)
        search_box.send_keys(Keys.RETURN)

        # Wait for search results to load
        search_results = WebDriverWait(driver, 2).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "cite"))
        )

        links = []
        for result in search_results[:3]:
            link = result.text
            if link.startswith('http') and '.se' in link:
                links.append(link)

        return links
    except Exception as e:
        print(f"Error searching for {brand_domain}: {e}")
        return []

def read_brands(file_path):
    """
    Reads the brand names from a text file.
    """
    with open(file_path, 'r') as file:
        brands = [line.strip() for line in file]
    return brands

def generate_domains(brands):
    """
    Generates .se domains for each brand.
    """
    domains = [f"{brand}.se" for brand in brands]
    return domains

def save_results_to_text(results, output_file):
    """
    Saves the search results to a text file.
    """
    with open(output_file, 'w') as file:
        for brand, links in results.items():
            if links:  # Only write brands with found links
                file.write(f"{brand}:\n")
                for link in links:
                    file.write(f"  {link}\n")

# Define file paths
brands_file = 'brands.txt'
output_file = 'brand_links.txt'

# Read brands from the text file
brands = read_brands(brands_file)

# Generate .se domains
domains = generate_domains(brands)

# Initialize the Chrome driver
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')  # Disable GPU usage
options.add_argument('--no-sandbox')  # Bypass OS security model
options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

driver = webdriver.Chrome(options=options)

# Search for each brand domain and save the results
results = {}
for domain in domains:
    links = search_brand_on_google(domain)
    results[domain] = links

# Close the driver
driver.quit()

# Save the results to a text file
save_results_to_text(results, output_file)

print(f"Data saved to {output_file}")
