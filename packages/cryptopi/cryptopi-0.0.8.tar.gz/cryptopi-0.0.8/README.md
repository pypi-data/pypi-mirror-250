### This project is a simple wrapper around the CoinMarketCap API.

### Installation

Install the package using pip:

```bash
pip install cryptopi
```

### Setup
Visit [Coin Market Cap Website](https://pro.coinmarketcap.com/), create an account, and get your API key.
Set your API key as an environment variable:

```bash
export CMC_PRO_API_KEY=<your_api_key>
````

Depending on how you use `cryptopi`, you may need to set the environment variable in your `.bashrc` or `.zshrc` file, or in your IDE's run configuration.

#

### Usage

```python
from cryptopi import CoinMarketCapApi
from cryptopi.models import Symbol
from cryptopi.utils import find_api_key

# Get your API key from environment variable.
API_KEY = find_api_key()

# Create an instance of the API.
api = CoinMarketCapApi(API_KEY)

# Optionally filter by symbol.
filters = {
    'symbol': [Symbol.BTC, Symbol.ETH]
}

# Get the latest quotes.
quotes = api.cryptocurrency_latest_quotes(**filters)

# The last call returns a `cryptopi.api.urls.responses.QuoteResponse` instance.
# This can be used directly, or as a dictionary.
quotes_dict = quotes.as_dict()
```