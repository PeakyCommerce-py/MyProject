import pandas as pd

def transform_csv(input_file, output_file):
    # Read the input CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # Prepare a list to store the transformed strings
    output_strings = []

    # Iterate through each row in the DataFrame
    for _, row in df.iterrows():
        row_properties = []
        for header, value in row.items():
            # Skip empty values
            if pd.notnull(value) and str(value).strip():
                # Format as 'Produktinformation_{key}_{value}'
                formatted_string = f"Produktinformation_{header}_{value}"
                row_properties.append(formatted_string)
        # Combine all key-value pairs in the row with commas
        output_strings.append(", ".join(row_properties))

    # Create a new DataFrame with the transformed properties
    transformed_df = pd.DataFrame({'Transformed_Properties': output_strings})

    # Save the transformed properties to a CSV file
    transformed_df.to_csv(output_file, index=False)
    print(f"Transformation complete. Output saved to {output_file}.")

# Main execution
if __name__ == '__main__':
    # Specify the input and output file paths
    input_file = "Deokej.csv"  # Replace with the path to your CSV file
    output_file = "output_Deokej.csv"  # Replace with the desired output file path

    # Run the transformation
    transform_csv(input_file, output_file)
