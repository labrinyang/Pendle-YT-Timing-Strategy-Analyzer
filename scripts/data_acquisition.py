import requests
import pandas as pd
import numpy as np
from datetime import datetime, timezone
from requests.adapters import HTTPAdapter
from dateutil import parser
import random
import time
import io
import json


class DataAcquisition:
    def __init__(self, market_contract, yt_contract, start_time_str, network='ethereum'):
        """
        Initialize the DataAcquisition class with the required parameters.
        
        :param market_contract: The market contract address.
        :param yt_contract: The YT contract address.
        :param start_time_str: The start time in ISO format (e.g., '2023-01-01T00:00:00.000Z').
        :param network: The network name ('ethereum', 'arbitrum', or 'mantle').
        """
        self.session = self._init_session()
        self.market_contract = market_contract.lower()
        self.yt_contract = yt_contract.lower()
        self.start_time_str = start_time_str
        self.end_time_str = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')
        self.network_id = self._get_network_id(network)
        self.headers = {
            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          f"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(80, 100)}.0.{random.randint(1000, 2000)}.0 Safari/537.36"
        }
        # Construct URLs
        self.url_apy = f'https://api-v2.pendle.finance/core/v1/{self.network_id}/markets/{self.market_contract}/apy-history-1ma'
        self.url_ohlcv = f'https://api-v2.pendle.finance/core/v3/{self.network_id}/prices/{self.yt_contract}/ohlcv'
        self.url_transactions = f'https://api-v2.pendle.finance/core/v3/{self.network_id}/transactions'

    @staticmethod
    def _init_session():
        """Initialize the session with retry capability."""
        session = requests.Session()
        retry_strategy = requests.packages.urllib3.util.retry.Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = requests.adapters.HTTPAdapter(max_retries=retry_strategy)
        session.mount('https://', adapter)
        session.mount('http://', adapter)
        return session

    @staticmethod
    def _get_network_id(network):
        """Retrieve the network ID based on the network name."""
        network_ids = {
            'arbitrum': '42161',
            'ethereum': '1',
            'mantle': '5000'
        }
        network_id = network_ids.get(network.lower())
        if network_id is None:
            raise ValueError(f"Unsupported network type: {network}")
        return network_id

    def fetch_transactions(self, limit=1000, max_attempts=1, retry_delay=5):
        """
        Fetch as many transactions as possible by handling pagination and rate limits.
        
        :param limit: Number of transactions to fetch per request (max 1000).
        :param max_attempts: Max number of retry attempts in case of 429 or other errors.
        :param retry_delay: Initial delay between retries when rate limit is hit (in seconds).
        :return: DataFrame containing the transactions data.
        """
        all_transactions = []
        skip = 0
        attempts = 0

        while True:
            params = {
                'market': self.market_contract,
                'action': 'SWAP_PT,SWAP_PY,SWAP_YT',
                'origin': 'PENDLE_MARKET,YT',
                'skip': str(skip),
                'limit': str(limit),
                'minValue': '0'
            }

            try:
                response = self.session.get(self.url_transactions, headers=self.headers, params=params)
                response.raise_for_status()

                data = response.json()
                transactions = data.get('results', [])
                if not transactions:
                    break

                df_transactions = pd.DataFrame(transactions)
                df_transactions['timestamp'] = pd.to_datetime(df_transactions['timestamp'], utc=True)
                all_transactions.append(df_transactions)

                # Update skip for pagination
                skip += limit
                attempts = 0  # Reset attempts after a successful request

                # Introduce a random delay to avoid rate limiting
                random_delay = random.uniform(0.15, 0.55)
                time.sleep(random_delay)

            except requests.HTTPError as e:
                if response.status_code == 400:
                    attempts += 1
                    if attempts > max_attempts:
                        break
                    wait_time = retry_delay * (2 ** (attempts - 1))
                    random_extra_delay = random.uniform(1, 5)
                    time.sleep(wait_time + random_extra_delay)
                else:
                    break
            except Exception as e:
                attempts += 1
                if attempts > max_attempts:
                    break
                random_failure_delay = random.uniform(5, 10)
                time.sleep(random_failure_delay)

        if all_transactions:
            return pd.concat(all_transactions, ignore_index=True)
        else:
            return pd.DataFrame()

    def fetch_ohlcv(self):
        """
        Fetch OHLCV data for the YT contract.
        
        :return: DataFrame containing the OHLCV data.
        """
        params = {
            "time_frame": "hour",
            "timestamp_start": self.start_time_str,
            "timestamp_end": self.end_time_str
        }
        try:
            response = self.session.get(self.url_ohlcv, headers=self.headers, params=params)
            response.raise_for_status()
            results = response.json().get('results', [])
            data = []
            for item in results:
                time = datetime.fromisoformat(item['time'].rstrip('Z'))
                data.append([time, float(item['open']), float(item['high']), float(item['low']),
                             float(item['close']), float(item.get('volume', 0))])
            df_ohlcv = pd.DataFrame(data, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            df_ohlcv['Time'] = df_ohlcv['Time'].dt.tz_localize('UTC')
            return df_ohlcv
        except requests.RequestException as e:
            return pd.DataFrame()

    def fetch_apy(self):
        """
        Fetch APY data for the market contract.
        
        :return: DataFrame containing the APY data.
        """
        params = {
            "time_frame": "hour",
            "timestamp_start": self.start_time_str,
            "timestamp_end": self.end_time_str
        }
        try:
            response = self.session.get(self.url_apy, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            csv_data = data.get('results', '')
            if csv_data:
                df = pd.read_csv(io.StringIO(csv_data))
                df['Time'] = pd.to_datetime(df['timestamp'], unit='s', utc=True)
                df.drop(columns=['timestamp'], inplace=True)
                return df
            else:
                return pd.DataFrame()
        except requests.RequestException as e:
            return pd.DataFrame()

    def run(self):
        """
        Execute the data retrieval process and combine the results.
        
        :return: Tuple of DataFrames (df_combined, df_transactions).
        """
        df_apy = self.fetch_apy()
        df_ohlcv = self.fetch_ohlcv()

        if not df_apy.empty and not df_ohlcv.empty:
            df_combined = pd.merge_asof(
                df_apy.sort_values('Time'),
                df_ohlcv.sort_values('Time'),
                on='Time'
            )
            self.df_combined = df_combined
            df_transactions = self.fetch_transactions()
            return df_combined, df_transactions
        else:
            return pd.DataFrame(), pd.DataFrame()


def clean_transaction_data(df_transactions):
    """
    Cleans the transaction data by expanding nested columns and normalizing values.
    
    :param df_transactions: Raw transaction DataFrame.
    :return: Cleaned DataFrame.
    """
    df_tran_cleaned = df_transactions.copy()
    
    # Parse the 'market' field
    df_tran_cleaned['market'] = df_tran_cleaned['market'].astype(str).apply(lambda x: json.loads(x.replace("'", '"')))
    market_df = pd.json_normalize(df_tran_cleaned['market'])
    market_df.columns = [f"market_{col}" for col in market_df.columns]
    df_tran_cleaned = df_tran_cleaned.drop('market', axis=1).join(market_df)

    # Expand the 'inputs' and 'outputs' fields
    df_tran_cleaned = expand_rows(df_tran_cleaned, 'inputs', ['input_address', 'input_baseType'])
    df_tran_cleaned = expand_rows(df_tran_cleaned, 'outputs', ['output_address', 'output_baseType'])

    # Clean the 'valuation' field
    df_tran_cleaned['valuation'] = df_tran_cleaned['valuation'].astype(str).apply(lambda x: json.loads(x.replace("'", '"')))
    valuation_df = pd.json_normalize(df_tran_cleaned['valuation'])
    valuation_df.columns = [f"valuation_{col}" for col in valuation_df.columns]
    df_tran_cleaned = df_tran_cleaned.drop('valuation', axis=1).join(valuation_df)

    df_tran_cleaned['timestamp'] = pd.to_datetime(df_tran_cleaned['timestamp'])

    # Convert columns with lists to strings to make them hashable
    for col in df_tran_cleaned.columns:
        if df_tran_cleaned[col].apply(lambda x: isinstance(x, list)).any():
            df_tran_cleaned[col] = df_tran_cleaned[col].apply(lambda x: str(x) if isinstance(x, list) else x)

    # Now, we can safely drop duplicates
    df_tran_cleaned = df_tran_cleaned.drop_duplicates()
    
    return df_tran_cleaned



def expand_rows(df, col_name, new_cols):
    """
    Expands rows in a DataFrame where a column contains lists of dictionaries.
    
    :param df: DataFrame to expand.
    :param col_name: Column name to expand.
    :param new_cols: New column names for the expanded data.
    :return: Expanded DataFrame.
    """
    expanded_rows = []
    for _, row in df.iterrows():
        items_list = row[col_name]
        if isinstance(items_list, list):
            for item in items_list:
                expanded_row = row.to_dict()
                expanded_row[new_cols[0]] = item.get('asset', {}).get('address')
                expanded_row[new_cols[1]] = item.get('asset', {}).get('baseType')
                expanded_rows.append(expanded_row)
        else:
            expanded_rows.append(row.to_dict())
    return pd.DataFrame(expanded_rows)


# Example usage
if __name__ == "__main__":
    # Sample parameters
    market_contract = "0x36d3ca43ae7939645c306e26603ce16e39a89192"
    yt_contract = '0xeb993b610b68f2631f70ca1cf4fe651db81f368e'
    start_time = "2023-01-01T00:00:00.000Z"
    network = "ethereum"

    # Initialize and run data acquisition
    data_acquisition = DataAcquisition(market_contract, yt_contract, start_time, network)
    df_combined, df_transactions = data_acquisition.run()

    # Clean transaction data
    df_cleaned_transactions = clean_transaction_data(df_transactions)

    # Print a sample of the cleaned data
    print(df_cleaned_transactions.head())
