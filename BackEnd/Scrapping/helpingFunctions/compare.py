import pandas as pd

def compare_csv(file1, file2):
    # Read CSV files
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Ensure that both DataFrames have the same column order
    if list(df1.columns) != list(df2.columns):
        print("The columns in the files do not match. Please ensure both files have the same columns.")
        return

    # Find common rows between both dataframes
    common_rows = df1.merge(df2, how='inner')
    
    # Remove duplicates to ensure we only count unique identical rows
    common_rows.drop_duplicates(inplace=True)

    # Print the number of common rows
    print(f"Number of identical rows: {len(common_rows)}")

# Replace 'file1.csv' and 'file2.csv' with the paths to your CSV files
# compare_csv('TotalData.csv', 'EbayCellPhoneData.csv')


def count_repeating_rows(file):
    # Read the CSV file
    df = pd.read_csv(file)

    # Count rows and find duplicates
    duplicate_rows = df[df.duplicated(keep=False)]

    # Count total repeating rows
    num_repeating_rows = len(duplicate_rows)

    print(f"Number of repeating rows: {num_repeating_rows}")

# Replace 'file.csv' with the path to your CSV file
count_repeating_rows('Scraped.csv')
