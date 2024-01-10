# Subsets Python Client

Easily access the Subsets data warehouse using Python. For more details and features, visit [subsets.io](https://www.subsets.io)

## Installation

Run the following command to install the API:

```pip install subsetsio```
## Usage

At the moment, you can only use the SDK for querying. To explore datasets, checking quotas, and viewing past queries, visit the [subsets.io](https://www.subsets.io) web interface.

```python
import subsetsio

# Temp API Key. Sign up for a free permanent key.
client = subsetsio.Client(api_key="YOUR_API_KEY")
df = client.query(sql_query)
```

## License

[MIT Licensed](LICENSE.md)