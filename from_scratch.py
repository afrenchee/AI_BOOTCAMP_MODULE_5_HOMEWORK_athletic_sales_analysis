import os, sys
import pandas as pd
from fuzzywuzzy import process

windows_is_the_OS = False

def clear_screen():
    if windows_is_the_OS:
        os.system('cls')
    else:
        os.system('clear')

def end_program():
    if windows_is_the_OS:
        os.system('dir')
    else:
        os.system('pwd')
        os.system('ls')
    print("")
    sys.exit()

if __name__ == '__main__':
    clear_screen()

    print("\n\nWELCOME TO MODULE 5'S HOMEWORK SUBMISSION FROM AUSTIN FRENCH!!!\n")

    # Combine and Clean the Data:
    df_2020 = pd.read_csv('./Resources/athletic_sales_2020.csv')
    df_2021 = pd.read_csv('./Resources/athletic_sales_2021.csv')

    # Check that the columns in the two DataFrames have similar names and data types.
    print("\n2020 Columns:\n", df_2020.columns, "\n")
    print("2021 Columns:\n", df_2021.columns, "\n")
    print("2020 Data Types:\n", df_2020.dtypes, "\n")
    print("2021 Data Types:\n", df_2021.dtypes, "\n")

    # Combine the two DataFrames by the rows using an inner join, and reset the index.
    df_combined = pd.concat([df_2020, df_2021], ignore_index=True)

    # Check if there are any null values.
    print("Null values check:\n", df_combined.isnull().sum(), "\n")

    # Check each column’s data type.
    print("Combined Data Types:\n", df_combined.dtypes, "\n")

    # Convert the "invoice_date" column to a datetime data type, specifying the format to prevent parsing issues.
    df_combined['invoice_date'] = pd.to_datetime(df_combined['invoice_date'], format='%m/%d/%y', errors='coerce')

    # Confirm that the data type has been changed.
    print("Confirmed `invoice_date` dtype:", df_combined['invoice_date'].dtype, "\n")

    # Print unique product names to debug the 'Women’s Athletic Footwear' issue
    print("Unique product names:\n", df_combined['product'].unique(), "\n")

    # Ensure that the 'product' column has no trailing whitespaces or case sensitivity issues
    df_combined['product'] = df_combined['product'].str.strip()

    # Use fuzzy matching to find close matches to 'Women’s Athletic Footwear'
    query_product = "Women’s Athletic Footwear"
    product_choices = df_combined['product'].unique()

    # Find the closest match
    best_match = process.extractOne(query_product, product_choices)
    print(f"Best match for '{query_product}': {best_match}\n")

    # If the match is good (above a certain threshold), use it
    if best_match[1] > 80:  # Threshold of 80% match
        df_womens_footwear = df_combined[df_combined['product'] == best_match[0]]
        print(f"Filtered data using best match '{best_match[0]}' for 'Women’s Athletic Footwear'.\n")
    else:
        print(f"No good match found for 'Women’s Athletic Footwear'. Closest match was '{best_match[0]}'.\n")
        df_womens_footwear = pd.DataFrame()  # Empty DataFrame to prevent further operations

    if df_womens_footwear.empty:
        print("No data found for Women's Athletic Footwear after cleaning.")
    else:
        df_womens_retailer_sales = df_womens_footwear.groupby(['retailer', 'region', 'state', 'city']).agg({'total_sales': 'sum'}).reset_index()
        df_womens_retailer_sales.rename(columns={'total_sales': 'total_sales_amount'}, inplace=True)
        df_womens_retailer_sales = df_womens_retailer_sales.sort_values(by='total_sales_amount', ascending=False)
        top_5_womens_retailers = df_womens_retailer_sales.head(5)
        print("Top 5 Retailers with the Most Women's Athletic Footwear Sales:\n", top_5_womens_retailers, "\n")

        # Determine the Day with the Most Women's Athletic Footwear Sales:
        df_pivot_womens_sales = df_womens_footwear.pivot_table(index='invoice_date', values='total_sales', aggfunc='sum')
        df_pivot_womens_sales.rename(columns={'total_sales': 'total_sales_amount'}, inplace=True)
        df_daily_sales = df_pivot_womens_sales.resample('D').sum()

        # Check columns of df_daily_sales
        print("Columns of df_daily_sales:\n", df_daily_sales.columns, "\n")

        # Sort using the correct column name
        if 'total_sales_amount' in df_daily_sales.columns:
            df_top_10_days = df_daily_sales.sort_values(by='total_sales_amount', ascending=False).head(10)
            print("Top 10 Days with the Most Women's Athletic Footwear Sales:\n", df_top_10_days, "\n")

        # Determine the Week with the Most Women's Athletic Footwear Sales:
        df_weekly_sales = df_pivot_womens_sales.resample('W').sum()
        df_top_10_weeks = df_weekly_sales.sort_values(by='total_sales_amount', ascending=False).head(10)
        print("Top 10 Weeks with the Most Women's Athletic Footwear Sales:\n", df_top_10_weeks, "\n")

    end_program()
