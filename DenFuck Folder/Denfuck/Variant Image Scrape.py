from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up Selenium WebDriver
driver = webdriver.Chrome()
driver.get("https://royaldesign.se/path/to/product")  # Replace with actual URL

# Wait for images to load
time.sleep(3)  # Adjust as needed based on loading times

# Use CSS Selectors to find images with a specific pattern in their URL
image_elements = driver.find_elements(By.CSS_SELECTOR, 'img[src*="oyoy-rainbow"]')

# Extract image URLs
image_urls = [img.get_attribute('src') for img in image_elements]

# Print or save image URLs
for url in image_urls:
    print(url)

driver.quit()
