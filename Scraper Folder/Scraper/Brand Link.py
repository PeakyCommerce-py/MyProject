import re

def read_brands(file_path):
    """Read brand names from a text file."""
    with open(file_path, 'r') as file:
        brands = [line.strip() for line in file]
    return brands

def clean_brand_name(brand_name):
    """Remove special characters and replace spaces with hyphens."""
    # Remove special characters
    brand_name = re.sub(r'[^a-zA-Z0-9\s]', '', brand_name)
    # Replace spaces with hyphens and convert to lowercase
    brand_name = brand_name.replace(" ", "-").lower()
    return brand_name

def generate_urls(brands):
    """Generate URLs for each brand."""
    base_url = "https://www.kontorsgiganten.se/varumarken/{brand_name}"
    urls = [base_url.replace("{brand_name}", clean_brand_name(brand)) for brand in brands]
    return urls

def write_urls_to_txt(urls, output_path):
    """Write URLs to a text file."""
    with open(output_path, 'w') as file:
        for url in urls:
            file.write(url + '\n')

# Define file paths
brands_file = 'brands.txt'
output_file = 'urls.txt'

# Read brands from the text file
brands = read_brands(brands_file)

# Generate URLs
urls = generate_urls(brands)

# Write URLs to the text file
write_urls_to_txt(urls, output_file)

print(f"URLs written to {output_file}")
