import unittest
import os
import json
import redis
from pipeline import FoodPricesPipeline


class TestFoodPricesPipeline(unittest.TestCase):

    def setUp(self):
        self.fpl = FoodPricesPipeline()
        self.clear_queue(self.fpl.queue_name)
        self.clear_queue("candy")
        self.clear_queue("vegetable")
        self.clear_price_metrics()

    def tearDown(self):
        self.clear_queue(self.fpl.queue_name)
        self.clear_queue("candy")
        self.clear_queue("vegetable")
        self.clear_price_metrics()

    def clear_queue(self, queue):
        self.fpl.redis_client.delete(queue)

    def test_enqueue_dequeue(self):
        initial_length = self.get_queue_length()
        self.assertEqual(initial_length, 0)

        message = {"category": "vegetable", "price": 5.99}
        self.fpl.enqueue(message)

        length_after_enqueue = self.get_queue_length()
        self.assertEqual(length_after_enqueue, 1)

        dequeued_message = self.fpl.dequeue()

        length_after_dequeue = self.get_queue_length()
        self.assertEqual(length_after_dequeue, 0)

        self.assertEqual(json.loads(dequeued_message), message)

    def test_load_to_db(self):

        for i in range(30):
            self.fpl.redis_client.rpush("candy", 1)
            self.fpl.redis_client.rpush("vegetable", 2)

        self.assertEqual(30, self.get_cat_buffer_length("candy"))
        self.assertEqual(30, self.get_cat_buffer_length("vegetable"))

        self.fpl.load_to_db()

        self.assertEqual(0, self.get_cat_buffer_length("candy"))
        self.assertEqual(0, self.get_cat_buffer_length("vegetable"))

        candy_data = self.price_metrics("candy")
        vegetable_data = self.price_metrics("vegetable")

        self.assertEqual(len(candy_data), 1)
        self.assertEqual(len(vegetable_data), 1)
        self.assertEqual([("candy", 30.00, 1.00, 30)], candy_data)
        self.assertEqual([("vegetable", 60.00, 2.00, 30)], vegetable_data)

    def get_queue_length(self):
        return self.fpl.redis_client.llen(self.fpl.queue_name)

    def get_cat_buffer_length(self, cat):
        return self.fpl.redis_client.llen(cat)

    def price_metrics(self, cat):
        cur = self.fpl.pg_conn.cursor()
        cur.execute(
            """
            SELECT category, price_sum, price_avg, listings
            FROM price_metrics
            WHERE category = %s
        """,
            (cat,),
        )
        self.fpl.pg_conn.commit()
        res = cur.fetchall()
        cur.close()
        return res

    def clear_price_metrics(self):
        cur = self.fpl.pg_conn.cursor()
        cur.execute("DELETE FROM price_metrics where 1 = 1")
        self.fpl.pg_conn.commit()
        cur.close()


if __name__ == "__main__":
    unittest.main()
