import pandas as pd

# File paths
input_file = "345.csv"  # Replace with your input file
output_file = "Image Splitter.csv"  # Replace with your desired output file

# Read the CSV file
data = pd.read_csv(input_file)

# Dynamically identify image columns
ean_column = "EAN"  # Name of the column containing EAN
image_src_columns = [col for col in data.columns if col.startswith("Image Src")]
variant_image_columns = [col for col in data.columns if col.startswith("Variant Image")]

# Create a list to hold the rows for the result
result_rows = []

# Iterate through each row in the input file
for index, row in data.iterrows():
    ean = row[ean_column]  # Get the EAN value
    image_position = 1  # Start position at 1 for each EAN

    # Process Image Src columns
    for column in image_src_columns:
        image_src = row.get(column)  # Safely get the value from the column
        if pd.notna(image_src):  # Skip if the value is empty (NaN)
            result_rows.append({
                "EAN": ean,
                "Image Position": image_position,
                "Type": "Image Src",
                "Image URL": image_src
            })
            image_position += 1  # Increment the position for the next image

    # Process Variant Image columns
    for column in variant_image_columns:
        variant_image = row.get(column)  # Safely get the value from the column
        if pd.notna(variant_image):  # Skip if the value is empty (NaN)
            result_rows.append({
                "EAN": ean,
                "Image Position": image_position,
                "Type": "Variant Image",
                "Image URL": variant_image
            })
            image_position += 1  # Increment the position for the next image

# Convert the result list into a DataFrame
result = pd.DataFrame(result_rows)

# Save the result to a new CSV file
result.to_csv(output_file, index=False)

print(f"Formatted image data with sequential positions saved to {output_file}")
