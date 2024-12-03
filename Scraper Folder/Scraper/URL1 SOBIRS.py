import time
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import json

# Load search parameters from the JSON file
with open('parameters.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

search_parameters = data['searchParameters']
max_pages = int(data['pages'])
file_name = data['fileName']

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Open the main page to set cookies
driver.get('https://www.ratsit.se')
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, 'body'))
)  # Ensure the main page loads

# Load cookies from the JSON file
with open('cookies.json', 'r') as file:
    cookies = json.load(file)
    for cookie in cookies:
        cookie_with_name_and_value = {
            "name": cookie["name"],
            "value": cookie["value"]
        }
        if "domain" in cookie:
            cookie_with_name_and_value["domain"] = cookie["domain"]
        driver.add_cookie(cookie_with_name_and_value)

# Refresh the page after adding cookies
driver.refresh()
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, 'body'))
)

links = []

# Iterate through the specified search parameters
for params in search_parameters:
    person = params['person']
    amin = params['amin']
    amax = params['amax']
    m = params['m']
    k = params['k']
    b = params['b']
    r = params['r']
    er = params['er']
    eb = params['eb']

    # Initial URL (first page)
    url = f"https://www.ratsit.se/sok/person?vem={person}&m={m}&k={k}&r={r}&er={er}&b={b}&eb={eb}&amin={amin}&amax={amax}&fon=1&page=1"
    driver.get(url)
    time.sleep(10)

    try:
        # Ensure we are in the 'Personer' section
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.search-segment'))
        )
        segment = driver.find_element(By.CSS_SELECTOR, 'div.search-segment')
        buttons = segment.find_elements(By.TAG_NAME, 'button')
        personer_button = buttons[0]

        # Get total number of people from the 'Personer' button
        personer_text = personer_button.text  # e.g., "Personer: 15 st"
        total_people = int(personer_text.split(':')[1].strip().split(' ')[0])

        print(f"Total people found: {total_people}")

        # Calculate the number of pages needed (each page has up to 25 results)
        pages_needed = math.ceil(total_people / 25)
        pages_to_scrape = min(pages_needed, max_pages)
        print(f"Pages to scrape: {pages_to_scrape}")

        # Scrape the required number of pages
        for page in range(1, pages_to_scrape + 1):
            page_url = f"https://www.ratsit.se/sok/person?vem={person}&m={m}&k={k}&r={r}&er={er}&b={b}&eb={eb}&amin={amin}&amax={amax}&fon=1&page={page}"
            driver.get(page_url)
            time.sleep(3)
            # Wait for the search result list to load
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'search-result-list-holder'))
                )

                # Get page source and parse with BeautifulSoup
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                # Find the 'ul' with class 'search-result-list'
                ul = soup.find('ul', class_='search-result-list')
                if ul:
                    # Get all 'li' elements and then the first 'a' tag within each
                    li_elements = ul.find_all('li')
                    for li in li_elements:
                        a_tag = li.find('a')
                        if a_tag and 'href' in a_tag.attrs:
                            href = a_tag['href']
                            if href.startswith("/"):
                                href = f"https://www.ratsit.se{href}"
                            links.append(href)

                print(f"Page {page}: Collected {len(li_elements)} profile links.")

                # Check if we've collected all the results
                if len(links) >= total_people:
                    print("Collected all available people. Moving to next parameters.")
                    break

            except Exception as e:
                print(f"An error occurred on page {page}: {e}")

    except Exception as e:
        print(f"An error occurred while processing parameters {params}: {e}")

# Close the driver
driver.quit()

# Save the links to an Excel file
df = pd.DataFrame({'Links': links})
print(links)
excel_filename = f"{file_name}.xlsx"
df.to_excel(excel_filename, index=False)

print(f"Data saved to {excel_filename}")
