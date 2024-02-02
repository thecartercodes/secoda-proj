## crypto-table

This react table application reports the latest data points of the top 10 cryptocurrencies and refreshes every minute, roughly the
cadence at which the CoinMarketCap API refreshes.

We create a barebones backend in flask to act as a router for the API to avoid CORs complaints.

## Contributing

Prerequisites include `docker`. 

To develop locally:

1. Create a `.env.local` file from the sample `.env.sample` and replace with your personal
credentials. Source the local env file.

2. Use `make up` to start the services.

3. Run `make tests` to run tests.
