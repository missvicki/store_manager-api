"""Database models"""
from flask import Flask
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
                product_id SERIAL integer PRIMARY KEY UNIQUE , 
                product_name VARCHAR(50) UNIQUE NOT NULL, 
                category VARCHAR(50) UNIQUE NOT NULL, 
                unit_price integer NOT NULL, 
                quantity integer NOT NULL, 
                measure VARCHAR(12) NOT NULL);
            """
        )
        """create user table"""  
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL integer PRIMARY KEY UNIQUE, 
                name VARCHAR(50) NOT NULL, 
                password VARCHAR(12) UNIQUE NOT NULL, 
                role VARCHAR(15) NOT NULL);
            """
        )
        """create sales table"""  
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sales (
                sale_id SERIAL integer PRIMARY KEY UNIQUE, 
                product_id integer NOT NULL, 
                user_id integer NOT NULL,
                quantity integer NOT NULL,
                total integer NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                CONSTRAINT productid_foreign FOREIGN KEY (product_id) 
                    REFERENCES products(product_id) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE,
                CONSTRAINT userid_foreign FOREIGN KEY (user_id) 
                    REFERENCES users(user_id) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE);
            """
        )
        
    def insert_data_products(self):
        """inserts values into tables"""
        self.cursor.execute(
            """
            INSERT INTO products(product_name, category, unit_price, quantity, measure) 
                VALUES({}, '{}', '{}', {}, {}, '{}')"""
        )
    def insert_table(self, table):
    
        if table == "sales":
                self.cursor.execute(
                        """
                        INSERT INTO sales(sale_id, product_id, user_id, quantity, total, date) 
                            VALUES({}, {}, {}, {}, {}, '{}');
                        """
                    )

        if table == "users":
                self.cursor.execute(
                        """
                        INSERT INTO users(user_id, name, password, role) 
                            VALUES({}, '{}', '{}', '{}');
                        """
                    )
    
    def query_tables(self, table):
        """gets data in a table"""
        if table == "products":
            self.cursor.execute(
                "SELECT * FROM products"
            )
            products_ = self.cursor.fetchall()
            for _product_ in products_:
                print("product: {0}".format(_product_))
        if table == "sales":
            self.cursor.execute(
                "SELECT * FROM sales"
            )
            sales_ = self.cursor.fetchall()
            for _sale_ in sales_:
                print("sale: {0}".format(_sale_))
        if table == "users":
            self.cursor.execute(
                "SELECT * FROM users"
            )
            users_ = self.cursor.fetchall()
            for _user_ in users_:
                print("product: {0}".format(_user_))
    
    def update_data(self, table):
        """updates table record"""
        if table == "products":
            self.cursor.execute(
                # "UPDATE products SET product_name= iia WHERE product_id=1" 
            )
    
    def drop_table(self, table):
        """delete table"""
        if table == "products":
            self.cursor.execute("DROP TABLE products")
        
        if table == "sales":
            self.cursor.execute("DROP TABLE sales")

        if table == "users":
            self.cursor.execute("DROP TABLE users")   
