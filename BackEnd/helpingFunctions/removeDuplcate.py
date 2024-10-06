import pandas as pd

def merge_unique_csv(file1, file2, file3, output_file):
    # Read CSV files
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    df3 = pd.read_csv(file3)

    # Concatenate all three dataframes
    combined_df = pd.concat([df1, df2, df3], ignore_index=True)

    # Drop duplicate rows
    unique_df = combined_df.drop_duplicates()

    # Save the unique rows to a new CSV file
    unique_df.to_csv(output_file, index=False)

    print(f"New file '{output_file}' created with unique rows.")

# Replace 'file1.csv', 'file2.csv', 'file3.csv', and 'output.csv' with your file paths
merge_unique_csv('EbayCellPhoneData.csv', 'TotalScrappedData.csv', 'TotalData.csv', 'Scraped.csv')
