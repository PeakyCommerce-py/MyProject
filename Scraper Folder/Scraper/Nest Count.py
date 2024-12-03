from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

# Set up the Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(options=options)


def get_product_count(brand_url):
    """
    Goes to the brand URL and scrapes the product count from the page.
    """
    try:
        driver.get(brand_url)

        # Wait for the product count element to load (using a max wait of 10 seconds)
        product_count_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='mg p tn']"))
        )

        # Extract the text and get the number of products
        product_count_text = product_count_element.text
        product_count = re.findall(r'\d+', product_count_text)[0]  # Extract the first number found
        print(f"Extracted product count: {product_count} from {brand_url}")
        return product_count

    except Exception as e:
        print(f"Error scraping product count from {brand_url}: {e}")
        return "Error"


def read_links_from_file(file_path):
    """
    Reads the links from the text file where the links were stored.
    """
    with open(file_path, 'r') as file:
        links = [line.strip() for line in file if line.startswith('https')]  # Read only valid URLs
    return links


def save_product_counts_to_txt(counts, output_file):
    """
    Saves the brand names and their product counts to a text file.
    """
    with open(output_file, 'w') as file:
        file.write("Nest Product Count:\n")
        for brand, count in counts:
            file.write(f"{brand}: {count} products\n")


if __name__ == "__main__":
    try:
        # Read the brand URLs from the file
        links = read_links_from_file('Nordic_Nest_Links.txt')

        # List to store (brand URL, product count) tuples
        product_counts = []

        # Loop through each brand URL and scrape the product count
        for link in links:
            print(f"Processing: {link}")
            count = get_product_count(link)
            product_counts.append((link, count))

        # Save the results to a text file
        save_product_counts_to_txt(product_counts, 'Nest_Product_Count.txt')

        print(f"Scraping complete. Product counts saved to 'Nest_Product_Count.txt'.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the browser
        driver.quit()
