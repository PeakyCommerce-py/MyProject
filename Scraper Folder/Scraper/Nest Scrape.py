from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up the Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Initialize the Chrome WebDriver (change path if necessary)
driver = webdriver.Chrome(options=options)

def scrape_brand_links():
    # URL to scrape
    url = "https://royaldesign.se/varumarken"
    driver.get(url)

    # Wait for the page to load completely (adjust time if needed)
    time.sleep(5)

    # Find all anchor tags with href links under the section class "css-hwn5xc"
    brand_elements = driver.find_elements(By.XPATH, "//section[@class='css-hwn5xc']//a")

    # List to store all the href links
    links = []

    # Loop through each element and extract the href attribute
    for brand in brand_elements:
        try:
            href = brand.get_attribute('href')
            if href:
                full_link = f"https://royaldesign.se{href}"
                links.append(full_link)
        except Exception as e:
            print(f"Error extracting href: {e}")

    return links

def save_to_txt(links):
    # Save the links to a text file
    with open('Royal_Design_Links.txt', 'w') as file:
        file.write("Royal Design Links:\n")
        for link in links:
            file.write(f"{link}\n")

if __name__ == "__main__":
    try:
        # Scrape the brand links
        links = scrape_brand_links()

        # Save the links to a text file if found
        if links:
            save_to_txt(links)
            print(f"Scraping complete. Links saved to 'Royal_Design_Links.txt'")
        else:
            print("No links found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the driver
        driver.quit()
