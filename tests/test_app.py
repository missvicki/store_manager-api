"""Flask API Test doc for store manager"""

from copy import deepcopy

import unittest
import json
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from api.app import app
from api.models import DatabaseConnection

app.config['TESTING'] = True
class TestStoreManagerApi(unittest.TestCase):
    """TestStoreManagerApi(unittest.TestCase)--holds all tests we shall perform"""
    def setUp(self):
        """setUp(self)---"""
        self.db = DatabaseConnection()
        self.app = app.test_client()
        self.login_user = {
            "user_name": "vicky",
            "password":"victor"
        }
        self.user_data = {
            "name":"Vicky",
            "user_name":"vicky",
            "password":"victor",
            "role":"admin"
        }
        self.product = {
            "product_name": "Sugar",
            "category":"Food",
            "unit-price":4100,
            "quantity": 20,
            "measure":"Kgs"
        }
        self.sale = {
            "user_id":1,
            "product_id":1,
            "quantity":2
        }

    def test_get_all_products(self):
        """test_get_all_products(self)---"""
        response_products = self.app.get("/api/v1/products")
        data_products = json.loads(response_products.data())
        self.assertEqual(response_products.status_code, 200, msg="Found Products")

    def test_get_all_sales(self):
        """test_get_all_sales(self)---"""
        response_sales = self.app.get("/api/v1/sales")
        data_sales = json.loads(response_sales.data())
        self.assertEqual(response_sales.status_code, 200, msg="Found Sales")

    def test_get_one_product(self):
        """test__get_one_product(self)---"""
        productid = self.db.getProducts()[0]["product_id"]
        response_product = self.app.get("/api/v1/products/"+int(productid))
        data_products = json.loads(response_product.data())
        self.assertEqual(response_product.status_code, 200, msg="Found Product")

    def test_product_not_exist(self):
        """test_product_not_exist(self) --"""
        response_product = self.app.get("/api/v1/products/2")
        self.assertEqual(response_product.status_code, 404, msg="Didn't find product")
    
    def test_post_products_valid(self):
        """test_post_products(self)"""
        response_product = self.app.post("/api/v1/products",
                                      data=json.dumps(self.product),
                                      content_type='application/json')
        data = json.loads(response_product.data)
        self.product["product_id"] = 1
        self.assertEqual(response_product.status_code, 201, msg="product added")      

    def test_post_products_invalidmissing_data(self):
        """test_post_products(self)"""
        self.product["product_name"] = ""
        self.product["category"] = ""
        self.product["quantity"] = ""
        self.product["measure"] = ""
        self.product["unit_price"] = ""
        response_product = self.app.post("/api/v1/products",
                                      data=json.dumps(self.product),
                                      content_type='application/json')
        data = json.loads(response_product.data)
        self.product["product_id"] = 1
        self.assertEqual(response_product.status_code, 400, msg="product not added") 

    def test_post_products_invalid_data(self):
        """test_post_products(self)"""
        self.product["product_name"] = 2
        self.product["category"] = 6
        self.product["quantity"] = "2"
        self.product["measure"] = 36
        self.product["unit_price"] = "4100"
        response_product = self.app.post("/api/v1/products",
                                      data=json.dumps(self.product),
                                      content_type='application/json')
        data = json.loads(response_product.data)
        self.product["product_id"] = 1
        self.assertEqual(response_product.status_code, 400, msg="product not added") 
    
    # def test_edit_product(self):


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
        # PRODUCTS = self.backup_products
        # SALE = self.backup_sales


if __name__ == "__main__":
    unittest.main()
