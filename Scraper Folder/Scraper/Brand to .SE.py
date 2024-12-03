import pandas as pd

def read_brands(file_path):
    """
    Reads the brand names from a text file.
    """
    with open(file_path, 'r') as file:
        brands = [line.strip() for line in file]
    return brands

def generate_domains(brands):
    """
    Generates .se domains for each brand.
    """
    domains = [f"{brand}.se" for brand in brands]
    return domains

def save_results_to_excel(brands, domains, output_file):
    """
    Saves the results to an Excel file.
    """
    df = pd.DataFrame({'Brand': brands, 'Website': domains})
    df.to_excel(output_file, index=False)

# Define file paths
brands_file = 'brands.txt'
output_file = 'brand_websites.xlsx'

# Read brands from the text file
brands = read_brands(brands_file)

# Generate .se domains
domains = generate_domains(brands)

# Save the results to an Excel file
save_results_to_excel(brands, domains, output_file)

print(f"Data saved to {output_file}")
