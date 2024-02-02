## pubsub

This proof of concept illustrates a working example of a queuing mechanism using only python primitives and Redis.
For completeness, we also use postgres to show how batches of counting statistics on grocery listings can be buffered and dumped
into a database, perhaps hooked up with Secoda even, for analytics.

The system behaves as follows:

1. The pipeline's queue routes messages (i.e. jsons of food prices) to topics based on category. We use a mocked api to mimic a real life scenario where there might be a large volume of product listings for groceries ingested.

2. Unrecognized categories and malformed messages are funneled to the retry queue.

3. Recognized message formats are pushed to a secondary queue where counting statistics on listings are calculated and dumped into a database. 

## Contributing

Prerequisites include `docker` and optionally `psql` + `redis-cli` for cli in the terminal. 

To develop locally:

1. Use `make up` to start the services

2. Run the db migrations with `make migrate`

3. Run `make tests` to run the tests
