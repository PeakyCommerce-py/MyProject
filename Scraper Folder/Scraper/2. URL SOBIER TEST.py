import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json

# Load search parameters from the JSON file
with open('parameters.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

search_parameters = data['searchParameters']
pages = int(data['pages'])
file_name = data['fileName']

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Open the main page to set cookies
driver.get('https://www.ratsit.se')
time.sleep(5)

# Load cookies from the JSON file
with open('cookies.json', 'r') as file:
    cookies = json.load(file)
    for cookie in cookies:
        # Ensure cookies contain necessary attributes for Selenium
        cookie_with_name_and_value = {
            "name": cookie["name"],
            "value": cookie["value"]
        }
        if "domain" in cookie:
            cookie_with_name_and_value["domain"] = cookie["domain"]
        driver.add_cookie(cookie_with_name_and_value)

# Refresh the page after adding cookies
driver.refresh()
time.sleep(3)

links = []

# Iterate through the specified number of pages
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

    for page in range(1, pages + 1):
        url = f"https://www.ratsit.se/sok/person?vem={person}&m={m}&k={k}&r={r}&er={er}&b={b}&eb={eb}&amin={amin}&amax={amax}&fon=1&page={page}"

        # Open the URL
        driver.get(url)
        try:
            time.sleep(2)

            ul = driver.find_element(By.CLASS_NAME, 'search-result-list')
            search_results = ul.find_elements(By.TAG_NAME, 'a')

            for link in search_results:
                href = link.get_attribute('href')
                links.append(href)
            end_of_results_msg = driver.find_elements(By.CSS_SELECTOR, 'ul.search-result-list > li > p.mb-1')

            if end_of_results_msg and "Din sökning på person gav inga träffar" in end_of_results_msg[0].text:
                print(f"End of search results reached for current parameters. Moving to next parameters.")
                break

        except Exception as e:
            print(f"An error occurred on page {page}: {e}")

# Close the driver
driver.quit()

# Save the links to a text file
df = pd.DataFrame({'Links': links})
excel_filename = f"{file_name}.xlsx"
df.to_excel(excel_filename, index=False)

print(f"Data saved to {excel_filename}")
