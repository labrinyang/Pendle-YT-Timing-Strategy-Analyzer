import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from datetime import datetime, timezone
from dateutil import parser

class AssetRetriever:
    def __init__(self, network, base_type, contract_address):
        """
        Initializes the AssetRetriever class with network details and asset parameters.

        :param network: The name of the network (e.g., 'ethereum', 'arbitrum', 'mantle').
        :param base_type: The base type of the asset to filter (e.g., 'YT').
        :param contract_address: The contract address of the asset.
        """
        self.network = network.lower()
        self.base_type = base_type
        self.contract_address = contract_address.lower()
        self.session = self._init_session()
        self.network_id = self._get_network_id(self.network)
        self.url = f'https://api-v2.pendle.finance/core/v1{self.network_id}/assets/all'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        }

    @staticmethod
    def _init_session():
        """Initialize the session with retry mechanism."""
        session = requests.Session()
        retry = Retry(total=3, backoff_factor=1)
        session.mount('http://', HTTPAdapter(max_retries=retry))
        session.mount('https://', HTTPAdapter(max_retries=retry))
        return session

    @staticmethod
    def _get_network_id(network):
        """Retrieve the network ID based on the network name."""
        network_ids = {
            'arbitrum': '/42161',
            'ethereum': '/1',
            'mantle': '/5000'
        }
        network_id = network_ids.get(network.lower())
        if network_id is None:
            raise ValueError(f"Unsupported network type: {network}")
        return network_id

    @staticmethod
    def _parse_to_utc(date_str):
        """Convert a date string to a UTC datetime object."""
        dt = parser.parse(date_str)
        return dt.astimezone(timezone.utc)

    @staticmethod
    def _format_expiry(date_str):
        """Format the expiry date in a readable string format."""
        dt = AssetRetriever._parse_to_utc(date_str)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    def find_valid_assets(self):
        """Find valid assets matching the specified base type and contract address."""
        response = self.session.get(self.url, headers=self.headers)
        data = response.json()

        valid_assets = [
            {**item, 'expiry': self._format_expiry(item['expiry'])}
            for item in data
            if item.get('baseType') == self.base_type and
               item.get('address') == self.contract_address and
               'expiry' in item
        ]

        if not valid_assets:
            raise ValueError("No valid assets found with the given parameters")
        
        return valid_assets

    def get_asset_details(self):
        """Retrieve the symbol and expiry of the first valid asset."""
        valid_assets = self.find_valid_assets()
        symbol = valid_assets[0]['symbol']
        maturity = valid_assets[0]['expiry']
        return symbol, maturity


# Example Usage
if __name__ == "__main__":
    # Parameters for asset retrieval
    network = 'ethereum'
    base_type = 'YT'
    yt_contract = '0xeb993b610b68f2631f70ca1cf4fe651db81f368e'

    # Initialize the AssetRetriever
    asset_retriever = AssetRetriever(network, base_type, yt_contract)

    try:
        # Get the symbol and maturity (expiry date) of the asset
        symbol, maturity = asset_retriever.get_asset_details()
        print(f"Asset Symbol: {symbol}, Maturity Date: {maturity}")
    except ValueError as e:
        print(f"Error: {e}")
