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
output_file = "Image_Splitter.csv"  # Your output file stays the same

# Add error checking
if input_file is None:
    print("No CSV files found in directory")
    exit()
else:
    print(f"Using latest CSV file: {input_file}")

# Rest of your code remains the same...
# Read the CSV file
data = pd.read_csv(input_file)

# Dynamically identify Image Src columns
handle_column = "Handle"  # Name of the column containing Handle
image_src_columns = [col for col in data.columns if col.startswith("Image Src")]

# Create a list to hold the rows for the result
result_rows = []

# Iterate through each row in the input file
for index, row in data.iterrows():
    handle = row[handle_column]  # Get the Handle value

    # Initialize position counter for Image Src
    image_src_position = 1

    # Process Image Src columns
    for column in image_src_columns:
        image_src = row.get(column)  # Safely get the value from the column
        if pd.notna(image_src):  # Skip if the value is empty (NaN)
            result_rows.append({
                "Handle": handle,  # Use Handle value
                "Image Position": image_src_position,
                "Type": "Image Src",
                "Image URL": image_src
            })
            image_src_position += 1  # Increment the position for Image Src

# Convert the result list into a DataFrame
result = pd.DataFrame(result_rows)

# Save the result to a new CSV file
result.to_csv(output_file, index=False)

print(f"Formatted image data saved to {output_file}")
