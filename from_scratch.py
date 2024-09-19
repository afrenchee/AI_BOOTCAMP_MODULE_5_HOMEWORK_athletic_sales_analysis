import os, sys
import pandas as pd

windows_is_the_OS = False  # This variable is set by the main programmer to ensure that Terminal / Command Prompt commands are correctly executed in clear_screen() and end_program()

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

	print("WELCOME TO MODULE 5'S HOMEWORK SUBMISSION FROM AUSTIN FRENCH!!!")

	# Combine and Clean the Data:
	# Import the two CSV files, athletic_sales_2020.csv and athletic_sales_2021.csv, and read them into DataFrames.
	df_2020 = pd.read_csv('./Resources/athletic_sales_2020.csv')
	df_2021 = pd.read_csv('./Resources/athletic_sales_2021.csv')

	# Check that the columns in the two DataFrames have similar names and data types.
	print("2020 Columns: ", df_2020.columns)
	print("2021 Columns: ", df_2021.columns)
	print("2020 Data Types:\n", df_2020.dtypes)
	print("2021 Data Types:\n", df_2021.dtypes)

	# Combine the two DataFrames by the rows using an inner join, and reset the index.
	df_combined = pd.concat([df_2020, df_2021], ignore_index=True)

	# Check if there are any null values.
	print("Null values check:\n", df_combined.isnull().sum())

	# Optional: Deal with null values (if required)
	# df_combined.dropna() or df_combined.fillna(method='ffill')

	# Check each column’s data type.
	print("Combined Data Types:\n", df_combined.dtypes)

	# Convert the "invoice_date" column to a datetime data type.
	df_combined['invoice_date'] = pd.to_datetime(df_combined['invoice_date'])

	# Confirm that the data type has been changed.
	print("Confirmed `invoice_date` dtype:", df_combined['invoice_date'].dtype)

	# Print unique product names to debug the 'Women’s Athletic Footwear' issue
	print("Unique product names:\n", df_combined['product'].unique())

	# Determine which Region Sold the Most Products:
	# Use either the groupby or pivot_table function to create a multi-index DataFrame with the "region", "state", and "city" columns.
	df_region_products = df_combined.groupby(['region', 'state', 'city']).agg({'units_sold': 'sum'}).reset_index()

	# Rename the aggregated column to reflect the aggregation of the data in the column.
	df_region_products.rename(columns={'units_sold': 'total_products_sold'}, inplace=True)

	# Sort the results in descending order to show the top five regions, including the state and city that have the greatest number of products sold.
	df_region_products = df_region_products.sort_values(by='total_products_sold', ascending=False)

	# Display the top five regions
	print("Top 5 Regions with the Most Products Sold:\n", df_region_products.head(5))

	# Determine which Region had the Most Sales:
	# Use either the groupby or pivot_table function to create a multi-index DataFrame with the "region", "state", and "city" columns.
	df_region_sales = df_combined.groupby(['region', 'state', 'city']).agg({'total_sales': 'sum'}).reset_index()

	# Rename the aggregated column to reflect the aggregation of the data in the column.
	df_region_sales.rename(columns={'total_sales': 'total_sales_amount'}, inplace=True)

	# Sort the results in descending order to show the top five regions, including the state and city that generated the most sales.
	df_region_sales = df_region_sales.sort_values(by='total_sales_amount', ascending=False)

	# Display the top five regions
	top_5_sales_regions = df_region_sales.head(5)
	print("Top 5 Regions with the Most Sales:\n", top_5_sales_regions)

	# Determine which Retailer had the Most Sales:
	# Use either the groupby or pivot_table function to create a multi-index DataFrame with the "retailer", "region", "state", and "city" columns.
	df_retailer_sales = df_combined.groupby(['retailer', 'region', 'state', 'city']).agg({'total_sales': 'sum'}).reset_index()

	# Rename the aggregated column to reflect the aggregation of the data in the column.
	df_retailer_sales.rename(columns={'total_sales': 'total_sales_amount'}, inplace=True)

	# Sort the results in descending order to show the top five retailers along with their region, state, and city that generated the most sales.
	df_retailer_sales = df_retailer_sales.sort_values(by='total_sales_amount', ascending=False)

	# Display the top five retailers
	top_5_retailers = df_retailer_sales.head(5)
	print("Top 5 Retailers with the Most Sales:\n", top_5_retailers)

	# Determine which Retailer Sold the Most Women's Athletic Footwear:
	# Filter the combined DataFrame to create a DataFrame with only women's athletic footwear sales data.
	df_womens_footwear = df_combined[df_combined['product'] == 'Women’s Athletic Footwear']

	# Use either the groupby or pivot_table function to create a multi-index DataFrame with the "retailer", "region", "state", and "city" columns.
	df_womens_retailer_sales = df_womens_footwear.groupby(['retailer', 'region', 'state', 'city']).agg({'total_sales': 'sum'}).reset_index()

	# Rename the aggregated column to reflect the aggregation of the data in the column.
	df_womens_retailer_sales.rename(columns={'total_sales': 'total_sales_amount'}, inplace=True)

	# Sort the results in descending order to show the top five retailers along with their region, state, and city that sold the most women's athletic footwear.
	df_womens_retailer_sales = df_womens_retailer_sales.sort_values(by='total_sales_amount', ascending=False)

	# Display the top five retailers for women's athletic footwear
	top_5_womens_retailers = df_womens_retailer_sales.head(5)
	print("Top 5 Retailers with the Most Women's Athletic Footwear Sales:\n", top_5_womens_retailers)

	# Determine the Day with the Most Women's Athletic Footwear Sales:
	# Create a pivot table with the "invoice_date" column as the index and the "total_sales" column as the values parameter.
	df_pivot_womens_sales = df_womens_footwear.pivot_table(index='invoice_date', values='total_sales', aggfunc='sum')

	# Rename the aggregated column to reflect the aggregation of the data in the column.
	df_pivot_womens_sales.rename(columns={'total_sales': 'total_sales_amount'}, inplace=True)

	# Apply the resample function to the pivot table, place the data into daily bins, and get the total sales for each day.
	df_daily_sales = df_pivot_womens_sales.resample('D').sum()

	# Sort the resampled DataFrame in descending order to show the top 10 days that generated the most women's athletic footwear sales.
	df_top_10_days = df_daily_sales.sort_values(by='total_sales_amount', ascending=False).head(10)

	# Display the top 10 days with the most women's athletic footwear sales
	print("Top 10 Days with the Most Women's Athletic Footwear Sales:\n", df_top_10_days)

	# Determine the Week with the Most Women's Athletic Footwear Sales:
	# Apply resample to the pivot table above, place the data into weekly bins, and get the total sales for each week.
	df_weekly_sales = df_pivot_womens_sales.resample('W').sum()

	# Sort the resampled DataFrame in descending order to show the top 10 weeks that generated the most women's athletic footwear sales.
	df_top_10_weeks = df_weekly_sales.sort_values(by='total_sales_amount', ascending=False).head(10)

	# Display the top 10 weeks with the most women's athletic footwear sales
	print("Top 10 Weeks with the Most Women's Athletic Footwear Sales:\n", df_top_10_weeks)

	end_program()




