"""Database models"""
from flask import Flask, jsonify
import psycopg2

from db import Products, Sales, Users

class DatabaseConnection:
    """Connect to the database"""
    def __init__(self):
        try:
            self.connection = psycopg2.connect(database='storemanager', user='postgres', password='admin', host='localhost', port='5432')
            self.connection.autocommit = True
            # allow you to read from and write to database
            self.cursor = self.connection.cursor()
        except psycopg2.DatabaseError as anything:
            print (anything)
    
    def create_tables(self):
        """create product table"""    
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                product_id SERIAL PRIMARY KEY UNIQUE , 
                product_name VARCHAR(50) UNIQUE NOT NULL, 
                category VARCHAR(50) UNIQUE NOT NULL, 
                unit_price integer NOT NULL, 
                quantity integer NOT NULL, 
                measure VARCHAR(12) NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            """
        )
        """create user table"""  
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY UNIQUE, 
                name VARCHAR(50) NOT NULL, 
                password VARCHAR(12) UNIQUE NOT NULL, 
                role VARCHAR(15) NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            """
        )
        """create sales table"""  
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sales (
                sale_id SERIAL PRIMARY KEY UNIQUE,  
                user_id integer NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                CONSTRAINT userid_foreign FOREIGN KEY (user_id) 
                    REFERENCES users(user_id) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE);
            """
        )
        """create sales has products table"""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS saleshasproducts(
                sale_id integer NOT NULL,
                product_id integer NOT NULL,
                quantity integer NOT NULL,
                total integer NOT NULL,
                CONSTRAINT sale_idforeignkey FOREIGN KEY (sale_id)
                    REFERENCES sales(sale_id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                CONSTRAINT prodidfk FOREIGN KEY (product_id)
                    REFERENCES products(product_id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            );
            """
        )
        
    def insert_data_products(self, data):
        """inserts values into table products"""
        self.cursor.execute(
            """
            INSERT INTO products(product_name, category, unit_price, quantity, measure, date) \
            VALUES('{}', '{}', {}, {}, '{}', '{}')""".format(data.product_name, data.category, data.unit_price, data.quantity, data.measure, data.date)
        )
    def check_product_exists_name(self, product_name):
        """check if product exists"""
        self.cursor.execute(
            "SELECT * FROM products WHERE product_name = '{}'", (product_name)
        )
        return self.cursor.fetchone()
    def getProducts(self):
        """get all products"""
        self.cursor.execute(
            "SELECT * FROM products"
        )
        _products = self.cursor.fetchall()
        for products in _products:
            return ("product: {0}".format(products)) 
    def getoneProduct(self, _pid):
        """get one product"""
        self.cursor.execute(
            "SELECT * FROM products WHERE product_id = %s", [_pid]
        )
        _products = self.cursor.fetchone()
        if _products:
            for products in _products:
                return ("product: {0}".format(products)) 
        else:
            return ("no product with that id")
    def deloneProduct(self, _pid):
        """delete one product"""
        self.cursor.execute(
            "DELETE FROM products WHERE product_id = %s", [_pid]
        )
    def check_product_exists_id(self, product_id):
        """check if product exists"""
        self.cursor.execute(
            "SELECT * FROM products WHERE product_id = %s", [product_id]) 
        return self.cursor.fetchone()   
    
    # def insert_table(self, table):
    
    #     if table == "sales":
    #             self.cursor.execute(
    #                     """
    #                     INSERT INTO sales(sale_id, product_id, user_id, quantity, total, date) 
    #                         VALUES({}, {}, {}, {}, {}, '{}');
    #                     """
    #                 )

    #     if table == "users":
    #             self.cursor.execute(
    #                     """
    #                     INSERT INTO users(user_id, name, password, role) 
    #                         VALUES({}, '{}', '{}', '{}');
    #                     """
    #                 )
    
    # def query_tables(self, table):
    #     """gets data in a table"""
    #     if table == "products":
    #         self.cursor.execute(
    #             "SELECT * FROM products"
    #         )
    #         products_ = self.cursor.fetchall()
    #         for _product_ in products_:
    #             print("product: {0}".format(_product_))
    #     if table == "sales":
    #         self.cursor.execute(
    #             "SELECT * FROM sales"
    #         )
    #         sales_ = self.cursor.fetchall()
    #         for _sale_ in sales_:
    #             print("sale: {0}".format(_sale_))
    #     if table == "users":
    #         self.cursor.execute(
    #             "SELECT * FROM users"
    #         )
    #         users_ = self.cursor.fetchall()
    #         for _user_ in users_:
    #             print("product: {0}".format(_user_))
    
    # def update_data(self, table):
    #     """updates table record"""
    #     if table == "products":
    #         self.cursor.execute(
    #             # "UPDATE products SET product_name= iia WHERE product_id=1" 
    #         )
    
    # def drop_table(self, table):
    #     """delete table"""
    #     if table == "products":
    #         self.cursor.execute("DROP TABLE products")
        
    #     if table == "sales":
    #         self.cursor.execute("DROP TABLE sales")

    #     if table == "users":
    #         self.cursor.execute("DROP TABLE users")   
