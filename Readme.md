# Rest API client for Trading212

Based on the new REST API of [Trading212](https://www.trading212.com/).

## Installation

```bash
pip install trading212-rest
```

## Usage

```python
from trading212_rest import Trading212

client = Trading212(token="your_api_token", demo=False)

orders = client.orders()

dividends = client.dividends()
```

This is just a small selection of functions. Most endpoints are already implemented.

For a full documentation on Trading212 endpoint paramaters see https://t212public-api-docs.redoc.ly/
