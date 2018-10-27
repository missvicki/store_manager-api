"""Flask API Test doc for store manager"""

from copy import deepcopy

import unittest
import json
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from api.app import PRODUCTS, SALES, app

BASE_URL_PRODUCTS = 'http://127.0.0.1:5000/api/v1/products'
BAD_ITEM_URL_PRODUCTS = '{}/16'.format(BASE_URL_PRODUCTS)
GOOD_ITEM_URL_PRODUCTS = '{}/10'.format(BASE_URL_PRODUCTS)

BASE_URL_SALES = 'http://127.0.0.1:5000/api/v1/sales'
BAD_ITEM_URL_SALES = '{}/4'.format(BASE_URL_SALES)
GOOD_ITEM_URL_SALES = '{}/3'.format(BASE_URL_SALES)

class TestStoreManagerApi(unittest.TestCase):
    """TestStoreManagerApi(unittest.TestCase)--holds all tests we shall perform"""
    def setUp(self):
        """setUp(self)---"""
        self.backup_products = deepcopy(PRODUCTS)
        self.backup_sales = deepcopy(SALES)
        self.app = app.test_client()
        self.app.testing = True

    def test_get_all_products(self):
        """test_get_all_products(self)---"""
        response_products = self.app.get(BASE_URL_PRODUCTS)
        data_products = json.loads(response_products.get_data())
        self.assertEqual(response_products.status_code, 200, msg="Found Products")
        self.assertEqual(len(data_products['products']), 11)

    def test_get_all_sales(self):
        """test_get_all_sales(self)---"""
        response_sales = self.app.get(BASE_URL_SALES)
        data_sales = json.loads(response_sales.get_data())
        self.assertEqual(response_sales.status_code, 200, msg="Found Sales")
        self.assertEqual(len(data_sales['sales']), 3)

    def test_get_one_product(self):
        """test__get_one_product(self)---"""
        response_product = self.app.get(BASE_URL_PRODUCTS)
        data_products = json.loads(response_product.get_data())
        self.assertEqual(response_product.status_code, 200, msg="Found Product")
        self.assertEqual(data_products['products'][0]['product_name'], 'Sugar')

    def test_product_not_exist(self):
        """test_product_not_exist(self) --"""
        response_product = self.app.get(BAD_ITEM_URL_PRODUCTS)
        self.assertEqual(response_product.status_code, 404, msg="Didn't find product")
    
    def test_post_products(self):
        """test_post_products(self)"""
        product = { "product_name": "Bic Pens",
                   "unit_price": 5000,
                   "quantity": 1, "category": "school", "measure": "boxes"}
        response_product = self.app.post(BASE_URL_PRODUCTS,
                                      data=json.dumps(product),
                                      content_type='application/json')
        data = json.loads(response_product.data)
        self.product["product_id"] = 1
        self.assertEqual(response_product.status_code, 201, msg="product added")
       
        print(data)

    def test_delete(self):
        response = self.app.delete(GOOD_ITEM_URL_PRODUCTS)
        self.assertEqual(response.status_code, 200, msg="Product has been deleted")
        response = self.app.delete(BAD_ITEM_URL_PRODUCTS)
        self.assertEqual(response.status_code, 404, msg="Product has not been deleted")

    def test_sale_not_exist(self):
        """test_sale_not_exist(self) --"""
        response_sale = self.app.get(BAD_ITEM_URL_SALES)
        self.assertEqual(response_sale.status_code, 404, "Didn't find sale")
    
    def test_post_sales(self):
        """test_post_sales(self)"""
        sale = {"sale_id": 4, "product_id": 6,
                "quantity": 1}
        response_sale = self.app.post(BASE_URL_SALES,
                                      data=json.dumps(sale),
                                      content_type='application/json')
        self.assertEqual(response_sale.status_code, 201, msg="sale added")
        data = json.loads(response_sale.get_data())
        print(data)

    def tearDown(self):
        """tearDown(self)---"""
        # reset app.products app.salesto initial state
        PRODUCTS = self.backup_products
        SALE = self.backup_sales


if __name__ == "__main__":
    unittest.main()
