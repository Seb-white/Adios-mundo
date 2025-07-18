# Fetch and calculate the average gasoline price in Colombia from datosabiertos.gov.co (JSON API)
import requests
import pandas as pd
from datetime import datetime, timedelta

# API endpoint for gasoline prices
API_URL = "https://www.datos.gov.co/resource/gjy9-tpph.json"

try:
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    # Convert 'precio' to numeric
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    # Build a date column from 'periodo' (year) and 'mes' (month)
    df['periodo'] = pd.to_numeric(df['periodo'], errors='coerce')
    df['mes'] = pd.to_numeric(df['mes'], errors='coerce')
    df['fecha'] = pd.to_datetime(df['periodo'].astype(str) + '-' + df['mes'].astype(str) + '-01')
    # Use the last 2 years
    # Fix: Use the first day of the current month for comparison, since data is monthly
    # Use the latest available date in the dataset as the end date
    latest_date = df['fecha'].max()
    two_years_ago = latest_date - pd.DateOffset(years=2)
    print(f"latest_date in dataset: {latest_date}")
    print(f"two_years_ago: {two_years_ago}")
    print("DataFrame sample:")
    print(df[['fecha', 'departamento', 'municipio', 'precio']].head(10))
    mask = (df['fecha'] >= two_years_ago) & (df['fecha'] <= latest_date)
    print(f"mask sum (rows in range): {mask.sum()}")
    period_prices = df.loc[mask, 'precio']
    avg_price = period_prices.mean()
    print(f"Average gasoline price in Colombia for the last 2 years: {avg_price:.2f} COP per gallon")
    print("\nPrices for the last 2 years:")
    print(df.loc[mask, ['fecha', 'departamento', 'municipio', 'precio']])
except Exception as e:
    print("Error fetching or processing data:", e)
