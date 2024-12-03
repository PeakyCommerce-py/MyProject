import pandas as pd
import glob
import os

# Function to get latest CSV
def get_latest_csv():
    directory = r"C:\Users\Dejan\PycharmProjects\GoogleSheet"
    csv_files = glob.glob(os.path.join(directory, "*.csv"))
    if not csv_files:
        return None
    return max(csv_files, key=os.path.getmtime)

# File paths
input_file = get_latest_csv()  # This will get the latest CSV file
output_file = "Tagar.csv"  # Your output file stays the same

# Add error checking
if input_file is None:
    print("No CSV files found in directory")
    exit()
else:
    print(f"Using latest CSV file: {input_file}")

# Rest of your code remains the same...
# Read the CSV file
data = pd.read_csv(input_file)

# Print the first few lines to check content
with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    if not lines:
        print("The input file is empty. Please provide a CSV file with data.")
        exit()
    else:
        print("First few lines of the file:")
        print(''.join(lines[:5]))

# Attempt to read the CSV file
try:
    data = pd.read_csv(input_file)
except pd.errors.EmptyDataError:
    print("No data found in the file. Please ensure the file is not empty.")
    exit()
except pd.errors.ParserError:
    print("Error parsing the file. Check if the delimiter is correct.")
    exit()

# Specify the columns to combine
columns_to_combine = ["a", "b", "c", "d", "e", "f"]  # Replace with actual column names

# Ensure the specified columns exist
missing_columns = [col for col in columns_to_combine if col not in data.columns]
if missing_columns:
    print(f"Missing columns in the input file: {missing_columns}")
    exit()

# Combine the columns row-wise with commas
data["Combined Category"] = data[columns_to_combine].apply(
    lambda row: ", ".join(row.dropna().astype(str)), axis=1
)

# Save the result to a new CSV file
data.to_csv(output_file, index=False)
print(f"Combined categories saved to {output_file}")