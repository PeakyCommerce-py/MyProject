import pandas as pd

# File paths
splitter_file = "Image_Splitter.csv"  # File with Handle, Image Position, and Image URL
original_file = "9.csv"  # File with Handle column
output_file = "Merged_Output.csv"  # Output file path

# Read the CSV files
splitter_data = pd.read_csv(splitter_file)
original_data = pd.read_csv(original_file)

# Create a list to store merged rows
merged_rows = []

# Ensure all columns from the original file are included in the new rows
original_columns = original_data.columns.tolist()

# Iterate over the rows in the original file
for _, original_row in original_data.iterrows():
    handle = original_row["Handle"]
    original_row_dict = original_row.to_dict()  # Convert to a dictionary

    # Check if Handle matches in the splitter file
    matching_rows = splitter_data[splitter_data["Handle"] == handle]

    if not matching_rows.empty:
        # Get all matching rows for the Handle
        matching_images = matching_rows.to_dict(orient="records")

        # Assign the first image URL and position to the existing row
        original_row_dict["Image Src"] = matching_images[0]["Image URL"]
        original_row_dict["Image Position"] = matching_images[0]["Image Position"]
        merged_rows.append(original_row_dict)

        # Add new rows for additional images (if any)
        for extra_image in matching_images[1:]:
            new_row = {col: "" for col in original_columns}  # Blank template
            new_row["Handle"] = handle
            new_row["Image Src"] = extra_image["Image URL"]
            new_row["Image Position"] = extra_image["Image Position"]
            merged_rows.append(new_row)
    else:
        # If no matching images, just add the original row as is
        merged_rows.append(original_row_dict)

# Create a DataFrame from the merged rows
merged_data = pd.DataFrame(merged_rows)

# Save the merged data to a CSV file
merged_data.to_csv(output_file, index=False)

print(f"Merged data saved to {output_file}")
