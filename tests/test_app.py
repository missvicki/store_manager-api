"""Flask API Test doc for store manager"""

from copy import deepcopy

import unittest
import json
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from api import app

BASE_URL_PRODUCTS = 'http://127.0.0.1:5000/storemanager/api/v1.0/products'
BAD_ITEM_URL_PRODUCTS = '{}/5'.format(BASE_URL_PRODUCTS)
GOOD_ITEM_URL_PRODUCTS = '{}/12'.format(BASE_URL_PRODUCTS)

BASE_URL_SALES = 'http://127.0.0.1:5000/storemanager/api/v1.0/sales'
BAD_ITEM_URL_SALES = '{}/5'.format(BASE_URL_SALES)
GOOD_ITEM_URL_SALES = '{}/3'.format(BASE_URL_SALES)

class TestStoreManagerApi(unittest.TestCase):
    """TestStoreManagerApi(unittest.TestCase)--holds all tests we shall perform"""
    def setUp(self):
        """setUp(self)---"""
        self.backup_products = deepcopy(app.PRODUCTS)
        self.backup_sales = deepcopy(app.SALES)
        self.app = app.app.test_client()
        self.app.testing = True

    def test_get_all_products(self):
        """test_get_all_products(self)---"""
        response_products = self.app.get(BASE_URL_PRODUCTS)
        data_products = json.loads(response_products.get_data())
        self.assertEqual(response_products.status_code, 200)
        self.assertEqual(len(data_products['products']), 12)

if __name__ == "__main__":
    unittest.main()
