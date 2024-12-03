import pandas as pd

# Load the CSV file
file_path = 'Brand_Bloomingville.csv'
data = pd.read_csv(file_path)


def extract_and_format(data, columns_to_extract, custom_format=None, level_delimiter=">"):
    """
    Extracts specified columns and formats data as needed.

    Parameters:
        data (DataFrame): The loaded CSV data.
        columns_to_extract (list): List of column headers to extract.
        custom_format (dict): Dictionary to apply custom formatting {column: format_function}.
        level_delimiter (str): Delimiter for hierarchical levels (default: ">").

    Returns:
        DataFrame: Processed data.
    """
    # Extract relevant columns
    extracted_data = data[columns_to_extract].copy()

    # Apply custom formatting if specified
    if custom_format:
        for column, formatter in custom_format.items():
            if column in extracted_data:
                extracted_data[column] = extracted_data[column].apply(formatter)

    return extracted_data


# Define which columns to extract for Shopify import
columns_to_extract = [
    "Product Code", "Brand", "Description-UK", "Selling Unit", "EAN Code"
]

# Example of custom formatting for a column (e.g., hierarchical formatting for categories)
custom_format = {
    "Description-UK": lambda x: f"Apparel & Accessories {level_delimiter} {x}" if pd.notna(x) else x
}

# Extract and format the data
formatted_data = extract_and_format(data, columns_to_extract, custom_format)

# Save to a new CSV file for Shopify import
formatted_data.to_csv("shopify_import_ready.csv", index=False)
print("Formatted data saved to 'shopify_import_ready.csv'")
