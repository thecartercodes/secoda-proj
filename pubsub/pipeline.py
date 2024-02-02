import json
import redis
import threading
import os
import logging
import time
import requests
import psycopg2


class FoodPricesPipeline:
    name = "Food Prices Pipeline"
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(name)

    def __init__(
        self,
    ):
        self.api_url = os.environ["APP_URL"]
        self.redis_host = os.environ["REDIS_HOST"]
        self.redis_port = os.environ["REDIS_PORT"]
        self.pg_dbname = os.environ["POSTGRES_DB"]
        self.pg_user = os.environ["POSTGRES_USER"]
        self.pg_password = os.environ["POSTGRES_PASSWORD"]
        self.pg_host = os.environ["POSTGRES_HOST"]
        self.pg_port = os.environ["POSTGRES_PORT"]

        # The categories we establish topics on to process
        # our messages for latest prices and counting statistics
        self.price_categories = ["candy", "vegetable"]

        # The amount of time to buffer the data for
        self.buffer_time = 10

        self.queue_name = "food_prices"

        self.redis_client = redis.StrictRedis(
            host=self.redis_host, port=self.redis_port
        )

        self.redis_lock = threading.Lock()

        self.pg_conn = psycopg2.connect(
            dbname=self.pg_dbname,
            user=self.pg_user,
            password=self.pg_password,
            host=self.pg_host,
            port=self.pg_port,
        )

        """
        This sets up our pipeline to work with mocked assets.
        Some work is needed to extend this to ingest
        data from an endpoint at a production scale.  
        """
        self.setup()

    def setup(self):
        threads = []
        # This is used to map the ingest thread to an endpoint
        endpoints = ["onion", "tomato", "lollipop", "chocolate", "shirt"]
        for i in range(5):
            thread = threading.Thread(target=self.request_msg, args=[endpoints[i]])
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def enqueue(self, msg):
        self.redis_client.rpush(self.queue_name, json.dumps(msg))
        self.logger.info(f" Queued - Message: {msg}")

    def dequeue(self):
        return self.redis_client.lpop(self.queue_name)

    def request_msg(self, endpoint):
        for i in range(10):
            response = requests.get(f"http://{self.api_url}/{endpoint}")
            self.enqueue(response.json())

    def process(self):
        start_time = time.time()
        while True:
            if time.time() - start_time >= self.buffer_time:
                self.load_to_db()
                start_time = time.time()

            msg = self.dequeue()
            if msg:
                json_msg = json.loads(msg)

                if json_msg["category"] in self.price_categories:
                    self.redis_client.rpush(json_msg["category"], json_msg["price"])
                    self.logger.info(f" Success - Processed Message: {msg} ")
                else:
                    self.redis_client.rpush("food_prices_retry_queue", msg)
                    self.logger.info(
                        f" Failed - Unrecognized Category, stored in retry queue - Message: {msg} "
                    )

    def load_to_db(self):
        for cat in self.price_categories:
            # This pipeline is important for avoiding race conditions
            # and wraps the range & delete in a transaction
            pipeline = self.redis_client.pipeline()

            pipeline.multi()

            pipeline.lrange(cat, 0, -1)
            pipeline.delete(cat)

            res = pipeline.execute()
            listings = res[0]

            prices = [float(elem.decode("utf-8")) for elem in listings]

            if len(prices) > 0:
                cursor = self.pg_conn.cursor()
                query = """
                    INSERT INTO price_metrics (
                        category,
                        price_sum,
                        price_avg,
                        listings,
                        published_at,
                        created_at
                    )
                    VALUES ('{cat}', {sum}, {sum} / {cnt} , {cnt} , to_timestamp({publish_ts}), now())
                """.format(
                    cat=cat, sum=sum(prices), cnt=len(prices), publish_ts=time.time()
                )
                cursor.execute(query)
                self.pg_conn.commit()
                self.logger.info(f" Success - Loaded into DB - {query}")
                cursor.close()

    def run(self):
        threads = []
        for i in range(5):
            thread = threading.Thread(target=self.process)
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()


if __name__ == "__main__":
    fpl = FoodPricesPipeline()
    fpl.run()
