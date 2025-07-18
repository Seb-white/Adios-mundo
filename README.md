## What does `.2f` mean in Python?

The `.2f` is a format specifier used in Python f-strings (and the `format()` method) to control how floating-point numbers are displayed.

- `.2f` means "format the number as a floating-point value with 2 digits after the decimal point".
- Example:
  ```python
  value = 1234.56789
  print(f"{value:.2f}")  # Output: 1234.57
  ```
This is useful for displaying prices or averages in a readable way, rounding to two decimal places.
## Explanation of `df.loc` and `mask`

### What is `mask`?
`mask` is a boolean Series (a list of True/False values) that is used to filter rows in a pandas DataFrame. It is created by applying a condition to one or more columns. For example:
```python
mask = (df['fecha'] >= two_years_ago) & (df['fecha'] <= latest_date)
```
This creates a mask that is True for rows where the 'fecha' (date) is within the last 2 years, and False otherwise.

### What is `df.loc`?
`df.loc` is a pandas method used to select rows and columns from a DataFrame by label. When combined with a mask, it selects only the rows where the mask is True. For example:
```python
df.loc[mask, ['fecha', 'departamento', 'municipio', 'precio']]
```
This returns only the rows (and specified columns) where the mask is True, i.e., the records within the desired date range.
## Explanation of Key Fixes and Changes

### 1. Date Filtering Logic
- The original script used the current date, which did not match the dataset’s latest available month, resulting in no data being selected.
- Fixed by using the latest date present in the dataset as the end of the 2-year range:
  ```python
  latest_date = df['fecha'].max()
  two_years_ago = latest_date - pd.DateOffset(years=2)
  mask = (df['fecha'] >= two_years_ago) & (df['fecha'] <= latest_date)
  ```

### 2. Debug Print Statements
- Added to help visualize what dates and data are being used:
  ```python
  print(f"latest_date in dataset: {latest_date}")
  print(f"two_years_ago: {two_years_ago}")
  print("DataFrame sample:")
  print(df[['fecha', 'departamento', 'municipio', 'precio']].head(10))
  print(f"mask sum (rows in range): {mask.sum()}")
  ```

### 3. Average Calculation and Output
- The script now calculates the average price only for the filtered period and prints the relevant records:
  ```python
  period_prices = df.loc[mask, 'precio']
  avg_price = period_prices.mean()
  print(f"Average gasoline price in Colombia for the last 2 years: {avg_price:.2f} COP per gallon")
  print(df.loc[mask, ['fecha', 'departamento', 'municipio', 'precio']])
  ```

These changes ensure the script works with the actual structure and time range of the dataset, providing correct results and helpful debug information.
# Gasoline Price Analysis in Colombia

This project provides a Python script to fetch, process, and analyze the average price of gasoline in Colombia using open data from the official government portal (datosabiertos.gov.co).

## Features
- Downloads the latest gasoline price data from the Colombian open data API (https://www.datos.gov.co/resource/gjy9-tpph.json).
- Processes the data using pandas, including conversion of price and date fields.
- Calculates the average gasoline price in Colombia for the last 2 years (using the most recent data available in the dataset).
- Prints a summary of the average price and a table of all records used in the calculation.
- Includes debug print statements to help understand the filtering and data processing steps.

## How it works
1. **Dependencies**: The script uses `requests` to fetch data and `pandas` for data processing. These are installed in your Python environment.
2. **Data Fetching**: The script downloads the JSON dataset from datosabiertos.gov.co, which contains monthly gasoline prices by department and municipality.
3. **Data Processing**:
    - Converts the 'precio' (price) field to numeric.
    - Combines 'periodo' (year) and 'mes' (month) into a proper date column.
    - Finds the latest available date in the dataset.
    - Filters the data to include only records from the last 2 years up to the latest available month.
4. **Analysis**:
    - Calculates the average price for the filtered period.
    - Prints the average and a table of all relevant records.
    - Debug print statements show key variables and a sample of the data for transparency.

## How to use
1. Make sure you have Python 3.7+ and the required packages (`requests`, `pandas`) installed.
2. Run the script `avg_gasoline_price.py` in your environment:
   ```
   python avg_gasoline_price.py
   ```
3. The script will output the average gasoline price for the last 2 years and show the records used in the calculation.

## Notes
- The script is designed for monthly data, as the dataset does not provide daily prices.
- If you want to analyze a specific city or department, you can further filter the DataFrame in the script.
- The script is robust to missing or malformed data, and will print errors if the data source changes format.

## Customization
- To analyze a different period, adjust the date filtering logic in the script.
- To use a different dataset, update the API URL and adjust the column names as needed.

---

If you have any questions or need further customization, feel free to ask!
