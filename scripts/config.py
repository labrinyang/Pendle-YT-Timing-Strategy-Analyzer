import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from datetime import datetime, timezone
import random


# Dictionary of network IDs
NETWORK_IDS = {
    'arbitrum': '/42161',
    'ethereum': '/1',
    'mantle': '/5000'
}


def init_session():
    """
    Initializes a session with retry capabilities to handle common HTTP errors.

    :return: A session object with retry logic enabled.
    """
    session = requests.Session()
    retry_strategy = Retry(
        total=3,  # Total number of retry attempts
        backoff_factor=1,  # Time between retries
        status_forcelist=[429, 500, 502, 503, 504],  # Status codes to trigger retries
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def get_network_id(network):
    """
    Retrieves the corresponding network ID for a given network name.

    :param network: Name of the blockchain network ('arbitrum', 'ethereum', 'mantle').
    :return: Network ID as a string.
    :raises ValueError: If the network is not supported.
    """
    network_id = NETWORK_IDS.get(network.lower())
    if network_id is None:
        raise ValueError("Invalid network: must be 'arbitrum', 'ethereum', or 'mantle'")
    return network_id


# Default configuration parameters
DEFAULT_CONFIG = {
    # Network settings
    'network': 'ethereum',
    'market_contract': '0x36d3ca43ae7939645c306e26603ce16e39a89192',
    'yt_contract': '0xeb993b610b68f2631f70ca1cf4fe651db81f368e',

    # Timing and data settings
    'start_time': "2023-01-01 00:00:00",  # Start time in human-readable format
    'underlying_amount': 1,  # Amount of underlying assets
    'points_per_hour_per_underlying': 0.04,  # Points earned per hour for each underlying asset
    'pendle_multiplier': 5,  # Pendle multiplier

    # Chart appearance settings
    'dark_mode': True,  # Enable or disable dark mode for charts

    # Headers for network requests, with a randomized User-Agent to avoid rate limiting
    'headers': {
        "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      f"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(80, 100)}.0.{random.randint(1000, 2000)}.0 Safari/537.36"
    }
}


def format_start_time(start_time_str):
    """
    Converts a human-readable datetime string into an ISO 8601 UTC string.

    :param start_time_str: Datetime string in the format 'YYYY-MM-DD HH:MM:SS'.
    :return: ISO 8601 formatted datetime string with milliseconds and 'Z' timezone indicator.
    """
    datetime_obj = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
    return datetime_obj.replace(tzinfo=timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')


def load_config(custom_config=None):
    """
    Loads the full configuration, combining default values with any custom overrides.

    :param custom_config: A dictionary of custom configuration values.
    :return: A dictionary containing the merged configuration.
    """
    # Start with the default config and update with any custom settings
    config = DEFAULT_CONFIG.copy()
    
    if custom_config:
        config.update(custom_config)
    
    # Format the start time and get the network ID
    config['start_time'] = format_start_time(config['start_time'])
    config['network_id'] = get_network_id(config['network'])
    
    return config


# Test block for the config script
if __name__ == "__main__":
    # Example of overriding configuration values
    custom_config = {
        'network': 'arbitrum',
        'market_contract': '0xNewMarketContract',
        'yt_contract': '0xNewYTContract',
        'start_time': "2022-06-01 00:00:00"
    }

    # Load the config with overrides
    config = load_config(custom_config)

    # Output the resulting configuration for debugging
    print("Loaded Configuration:")
    for key, value in config.items():
        print(f"{key}: {value}")

    # Test session initialization
    session = init_session()
    print("Session initialized successfully with retry strategy.")
