import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pandas as pd
import sys

# Use the Selector event loop on Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

not_array = ["Innehavare", "Delgivningsbar person", "Kommanditdelägare", "Bolagsman", "Styrelsesuppleant"]
okay_array = ["VD", "Vice VD", "Extern VD", "Extern Firmatecknare", "Firma tecknare", "Styrelseledamot", "Revisor",
              "Ordförande", "lekmannarevisor", "Likvidator", "Verklig Huvudman"]
# Ändra Markörer


def parse_number(string):
    """Parse a string into an integer, removing non-numeric characters, but keeping a leading minus for negative numbers."""
    # Check if the string starts with a minus sign
    is_negative = string.startswith('-')

    # Remove non-numeric characters (like spaces, commas, etc.)
    cleaned_string = ''.join(filter(str.isdigit, string))

    # Convert to integer and apply negative sign if necessary
    if cleaned_string:
        number = int(cleaned_string)
        return -number if is_negative else number
    else:
        return None


async def fetch(session, url):
    """Asynchronously fetch a URL using aiohttp."""
    async with session.get(url) as response:
        return await response.text()


async def parse_content_for_data(content, url):
    """Asynchronously parse the webpage content and extract data."""

    soup = BeautifulSoup(content, 'html.parser')
    data = {'URL': url}  # Include the URL in the data
    age_div = soup.find('div', class_='col-12 position-relative')
    if age_div:
        data['Age'] = age_div.p.text.strip()

    # Extract phone number
    target_divs = soup.find_all('div', class_='col-8')
    if len(target_divs) >= 2:
        second_div = target_divs[1]
        link = second_div.find('a')
        if link and link.get('href', '').startswith("tel:"):
            phone_number = link['href'][4:]
            if phone_number.startswith("+467"):
                data['Phone Number'] = phone_number.replace("-", "")

        else:
            return None
    else:
        return None
    # Find the desired information
    engagemang_div = soup.find('div', id='engagemang')
    if engagemang_div:
        rows = engagemang_div.find_all('tr')[1:]  # Skip the header row

        for row in rows:
            cols = row.find_all('td')
            if cols:
                # Check if phone number starts with '07' and status is 'Aktiv'
                if phone_number.startswith("+467"):
                    status = cols[2].get_text(strip=True)
                    if "Aktiv" in status:  # Check if status contains 'Aktiv'
                        omsattning = parse_number(cols[6].get_text(strip=True))
                        vinst = parse_number(cols[7].get_text(strip=True))

                        if omsattning is not None and vinst is not None:
                            Befattning = cols[3].get_text(strip=True)
                            if Befattning not in not_array:
                                if 100 <= omsattning <= 54000 or 54000 >= vinst >= 100 and 0 <= omsattning <= 54000:

                                    data['Status'] = status
                                    data['Befattning'] = cols[3].get_text(strip=True)
                                    data['Bokslut'] = cols[5].get_text(strip=True)
                                    data['Omsättning (KSEK)'] = cols[6].get_text(strip=True)
                                    data['Vinst (KSEK)'] = cols[7].get_text(strip=True)
                                    return data  # Return data for the first matching row

        return None  # Return None if no matching row is found
    else:
        return None


async def process_url(session, url, semaphore):
    """Process a single URL."""
    async with semaphore:
        try:
            content = await fetch(session, url)
            return await parse_content_for_data(content, url)
        except Exception as e:
            print(f"Error processing {url}: {e}")
            return None


async def process_urls(urls, max_concurrent_requests=10):
    """Process multiple URLs concurrently with a limit on the number of concurrent requests."""
    semaphore = asyncio.Semaphore(max_concurrent_requests)
    async with aiohttp.ClientSession() as session:
        tasks = [process_url(session, url, semaphore) for url in urls]
        return await asyncio.gather(*tasks)


def save_to_excel(data, filename='output.xlsx'):
    """Save the data to an Excel file."""
    # Filter out None values
    filtered_data = [item for item in data if item is not None]

    if not filtered_data:
        print("No valid data to save.")
        return

    df = pd.DataFrame(filtered_data)
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")


# Example usage
def load_urls_from_excel(filename):
    df = pd.read_excel(f"{filename}.xlsx", header=None)  # Assuming no header in the file
    urls = df.iloc[1:, 0].tolist()  # Skip the first row and take the first column

    # Convert each URL to string and remove the first and last two elements
    processed_urls = []
    for url in urls:
        if isinstance(url, str):
            processed_url = url  # Slicing each URL string
            processed_urls.append(processed_url)
    return processed_urls


excel_file_name = input("Enter the name of the Excel file (without .xlsx): ")
urls = load_urls_from_excel(excel_file_name)

# Increase the number of concurrent requests
data = asyncio.run(process_urls(urls, max_concurrent_requests=20))

name_file = input("Name collected data: ")

# Filter out None values before saving to Excel
save_to_excel(data, f"{name_file}.xlsx")
