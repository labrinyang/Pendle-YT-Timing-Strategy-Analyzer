# Import necessary modules
from scripts.asset_retriever import AssetRetriever
from scripts.data_acquisition import DataAcquisition, clean_transaction_data
from scripts.yt_calculation import YTCalculation
from scripts.plot_strategy import plot_yt_price_points_curve
import pandas as pd

from scripts.config import load_config 

# Load configuration from config.py
config = load_config()

# Extract the necessary parameters from the loaded config
network = config['network']
yt_contract = config['yt_contract']
market_contract = config['market_contract']
start_time = config['start_time']
underlying_amount = config['underlying_amount']
points_per_hour_per_underlying = config['points_per_hour_per_underlying']
pendle_multiplier = config['pendle_multiplier']
mode = 'plotly_dark' if config['dark_mode'] else 'plotly_white'


# Step 1: Retrieve Asset Information (Symbol, Maturity)
asset_retriever = AssetRetriever(network, 'YT', yt_contract)
try:
    symbol, maturity = asset_retriever.get_asset_details()
    print(f"Retrieved Asset - Symbol: {symbol}, Maturity Date: {maturity}")
except ValueError as e:
    print(f"Error retrieving asset details: {e}")

# Step 2: Fetch Data Using DataAcquisition
data_acquisition = DataAcquisition(market_contract, yt_contract, start_time, network)
df_combined, df_transactions = data_acquisition.run()

if df_combined.empty or df_transactions.empty:
    print("No data fetched from the API.")

# Step 3: Clean the Transaction Data
df_cleaned_transactions = clean_transaction_data(df_transactions)
if df_cleaned_transactions.empty:
    print("No valid transactions after cleaning.")
print(df_cleaned_transactions.columns)
print(df_combined.columns)

# Step 4: Merge cleaned transaction data with combined data
df_cleaned_transactions['timestamp'] = pd.to_datetime(df_cleaned_transactions['timestamp'], utc=True)
df_combined['timestamp'] = pd.to_datetime(df_combined['Time'], utc=True)

# Merge transaction data with combined data based on timestamp
df_merged = pd.merge_asof(df_cleaned_transactions.sort_values('timestamp'), 
                            df_combined[['timestamp', 'underlyingApy']],
                            on='timestamp',
                            direction='backward')

# Step 5: Perform YT Calculations
calculation = YTCalculation(df_merged, df_combined, maturity, points_per_hour_per_underlying, underlying_amount, pendle_multiplier)
df_merged, df_combined, h_range, fair_value_curve, weighted_points = calculation.run_calculations()

# Print the calculated data as a result
print(f"Total Weighted Points Per Underlying: {weighted_points}")
print(df_merged.head())
print(df_combined.head())

plot_yt_price_points_curve(df_merged, h_range, fair_value_curve, symbol, network, mode, underlying_amount)