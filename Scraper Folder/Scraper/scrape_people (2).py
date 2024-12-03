import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pandas as pd
import re  # Import the regular expression module at the top of your script

# Use the Selector event loop on Windows
import sys

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def fetch(session, url):
    """Asynchronously fetch a URL using aiohttp."""
    async with session.get(url) as response:
        return await response.text()


async def parse_content_for_telephone(content, url):
    """Asynchronously parse the webpage content to extract and validate the telephone number."""
    soup = BeautifulSoup(content, 'html.parser')
    data = {'URL': url}  # Include the URL in the data

    # Extract phone number
    target_divs = soup.find_all('div', class_='col-8')
    if len(target_divs) >= 2:
        second_div = target_divs[1]
        link = second_div.find('a')
        if link and link.get('href', '').startswith("tel:"):
            phone_number = link['href'][4:]
            if phone_number.startswith("+467"):
                data['Phone Number'] = phone_number.replace("-", "")
                return data
    return None


async def process_url(session, url):
    """Process a single URL."""
    try:
        content = await fetch(session, url)
        return await parse_content_for_telephone(content, url)
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None


async def process_urls(urls):
    """Process multiple URLs concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [process_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)


def save_to_excel(data, filename='output.xlsx'):
    """Save the data to an Excel file."""
    filtered_data = [item for item in data if item is not None]
    if not filtered_data:
        print("No valid data to save.")
        return

    df = pd.DataFrame(filtered_data)
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")


# Load URLs from an Excel file
def load_urls_from_excel(filename):
    df = pd.read_excel(f"{filename}.xlsx", header=None)  # Assuming no header in the file
    urls = df.iloc[1:, 0].tolist()  # Take the first column
    return urls


# Execution starts here
def clean_filename(filename):
    """Remove leading and trailing quotes from a filename."""
    return filename.strip("\"'")


# Execution starts here
excel_file_name_input = input("Enter the name of the Excel file (without .xlsx): ")
excel_file_name = clean_filename(excel_file_name_input)  # Clean the input

urls = load_urls_from_excel(excel_file_name)

data = asyncio.run(process_urls(urls))

name_file_input = input("Name the collected data file (without .xlsx): ")
name_file = clean_filename(name_file_input)  # Clean the input

# Save the collected data to Excel
save_to_excel(data, f"{name_file}.xlsx")
