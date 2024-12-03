import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pandas as pd
import os

# Define the base URL and the target URL template
base_url = 'https://proff.dk'
url_template = 'https://proff.dk/segmentering?revenueFrom=100&revenueTo=32000&page={page}'
cvr_base_url = 'https://datacvr.virk.dk/enhed/virksomhed/{cvr}?fritekst={cvr}&sideIndex=0&size=10'
page_log_file = 'last_page.txt'

async def fetch(session, url):
    async with session.get(url, ssl=False) as response:
        return await response.text()

async def fetch_company_details(session, company_url):
    company_response_text = await fetch(session, company_url)
    company_soup = BeautifulSoup(company_response_text, 'html.parser')

    company_cvr_span = company_soup.find('span', class_='MuiTypography-root MuiTypography-body1 companyId-data mui-1nzk1nd')

    company_cvr = None
    if company_cvr_span:
        company_cvr = company_cvr_span.text.strip()

    return company_cvr

def read_last_page():
    if os.path.exists(page_log_file):
        with open(page_log_file, 'r') as file:
            return int(file.read().strip())
    return 1

def save_last_page(page):
    with open(page_log_file, 'w') as file:
        file.write(str(page))

async def main():
    last_page = read_last_page()
    async with aiohttp.ClientSession() as session:
        all_crvs = []
        for page in range(last_page, last_page + 886):  # Adjust the range for the number of pages you want to scrape
            page_url = url_template.format(page=page)
            page_response_text = await fetch(session, page_url)
            soup = BeautifulSoup(page_response_text, 'html.parser')

            links = soup.find_all('a', class_='MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineHover mui-105wgyd')

            company_links = []
            for link in links:
                href = link.get('href')
                if href.startswith('/firma'):
                    full_url = f"{base_url}{href}"
                    company_links.append(full_url)

            tasks = [fetch_company_details(session, company_url) for company_url in company_links]
            results = await asyncio.gather(*tasks)

            crvs = [result for result in results if result]
            all_crvs.extend(crvs)

            # Save the last page
            save_last_page(page + 1)

        # Save CVR data to Excel
        df = pd.DataFrame(all_crvs, columns=['CVR'])
        df.to_excel('cvr_data.xlsx', index=False)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred: {e}")
