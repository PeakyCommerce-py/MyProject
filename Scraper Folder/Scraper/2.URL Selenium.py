import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json

# Function to get search parameters from the user
with open('parameters.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

search_parameters = data['searchParameters']
pages = int(data['pages'])
file_name = data['fileName']

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Open the login page
driver.get('https://www.ratsit.se')
time.sleep(5)

# Log in or use cookies if needed
with open('cookies.json', 'r') as file:
    cookies = json.load(file)
    for cookie in cookies:
        driver.add_cookie({"name": cookie["name"], "value": cookie["value"]})
time.sleep(3)
driver.refresh()

links = []

# Iterate through the specified search parameters
for params in search_parameters:
    person = params['person']
    amin = params['amin']
    amax = params['amax']
    m, k, b, r, er, eb = params['m'], params['k'], params['b'], params['r'], params['er'], params['eb']

    # Loop over pages
    for page in range(1, pages + 1):
        # Construct URL
        url = f"https://www.ratsit.se/sok/person?vem={person}&m={m}&k={k}&r={r}&er={er}&b={b}&eb={eb}&amin={amin}&amax={amax}&fon=1&page={page}"
        driver.get(url)

        try:
            # Wait for the "Personer" tab to appear and click it to ensure we're on the right section
            personer_tab = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Personer"))
            )
            personer_tab.click()

            # Wait for search results to load
            time.sleep(2)

            # Extract links
            ul = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'search-result-list'))
            )
            search_results = ul.find_elements(By.TAG_NAME, 'a')
            for link in search_results:
                links.append(link.get_attribute('href'))

            # Check for end of results on this page
            end_of_results_msg = driver.find_elements(By.CSS_SELECTOR, 'ul.search-result-list > li > p.mb-1')
            if end_of_results_msg and "Din sökning på person gav inga träffar" in end_of_results_msg[0].text:
                print(f"End of search results reached for current parameters. Moving to next parameters.")
                break

        except Exception as e:
            print(f"An error occurred on page {page}: {e}")

# Close the driver
driver.quit()

# Save the links to an Excel file
df = pd.DataFrame({'Links': links})
excel_filename = f"{file_name}.xlsx"
df.to_excel(excel_filename, index=False)

print(f"Data saved to {excel_filename}")
