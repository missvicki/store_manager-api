"""Database models"""
from flask import Flask, jsonify
import psycopg2
import datetime
from api.models import Products, Sales, Users, SalesHasProducts, Login
from api.config import env_config

class DatabaseConnection:
    """Connect to the database"""
    def __init__(self):
        self.connection = psycopg2.connect(database='storemanager', user='postgres', password='admin', host='localhost', port='5432')
        self.connection.autocommit = True
        # allow you to read from and write to database
        self.cursor = self.connection.cursor()
        try:
            databaseCredential = """
            database='storemanager_test_db'
            user='postgres' 
            password='admin'
            host='localhost'
            port='5432'
            """
            databaseCredential_ = """
            database='storemanager'
            user='postgres' 
            password='admin'
            host='localhost'
            port='5432'
            """
            _databaseCredential_ = """
            database='d5ll442t19st4t'
            user='ptlamqvmvizpvv' 
            password='ada2b20d19532983892990bc0262c38e6e2d68c9e491c191e556ee015491dfcb71min'
            host='ec2-23-23-101-25.compute-1.amazonaws.com'
            port='5432'
            uri='postgres://ptlamqvmvizpvv:a2b20d19532983892990bc0262c38e6e2d68c9e491c191e556ee015491dfcb71@ec2-23-23-101-25.compute-1.amazonaws.com:5432/d5ll442t19st4t'
            """
            if env_config['testing'] == True:
                self.connection = psycopg2.connect(databaseCredential)
                self.connection.autocommit = True
                # allow you to read from and write to database
                self.cursor = self.connection.cursor()

            # elif env_config['deploying'] == True:
            #     self.connection = psycopg2.connect(_databaseCredential_)
            #     self.connection.autocommit = True
            #     # allow you to read from and write to database
            #     self.cursor = self.connection.cursor()
            else:
                self.connection = psycopg2.connect(_databaseCredential_)
                self.connection.autocommit = True
                # allow you to read from and write to database
                self.cursor = self.connection.cursor()

        except psycopg2.DatabaseError as anything:
            print (anything)

    def drop_tables(self):
        """drop tables if exist"""

        self.cursor.execute(
            "DROP TABLE IF EXISTS products, users, sales, sales_has_products, login CASCADE"
        )

    def create_tables(self):
        """create product table""" 

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                product_id SERIAL PRIMARY KEY, 
                product_name VARCHAR(50) UNIQUE NOT NULL, 
                category VARCHAR(50) NOT NULL, 
                unit_price integer NOT NULL, 
                quantity integer NOT NULL, 
                measure VARCHAR(12) NOT NULL,
                date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                delete_status BOOLEAN DEFAULT FALSE);
            """
        )

        """create user table"""  
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY, 
                name VARCHAR(50) NOT NULL,
                user_name VARCHAR(12) NOT NULL UNIQUE, 
                password VARCHAR(12) UNIQUE NOT NULL, 
                role VARCHAR(15) NOT NULL,
                date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                delete_status BOOLEAN DEFAULT FALSE);
            """
        )

        """create sales table"""  
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sales (
                sale_id SERIAL PRIMARY KEY,  
                user_id integer NOT NULL,
                date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                delete_status BOOLEAN DEFAULT FALSE,
                CONSTRAINT userid_foreign FOREIGN KEY (user_id) 
                    REFERENCES users(user_id) 
                    ON UPDATE CASCADE);
            """
        )

        """create sales has products table"""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sales_has_products(
                sale_id integer NOT NULL,
                product_id integer NOT NULL,
                quantity integer NOT NULL,
                total integer NOT NULL,
                delete_status BOOLEAN DEFAULT FALSE,
                CONSTRAINT sale_idforeignkey FOREIGN KEY (sale_id)
                    REFERENCES sales(sale_id)
                    ON UPDATE CASCADE,
                CONSTRAINT prodidfk FOREIGN KEY (product_id)
                    REFERENCES products(product_id)
                    ON UPDATE CASCADE
            );
            """
        )

        """login table create"""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS login(
                user_name VARCHAR(12) NOT NULL,
                password VARCHAR(12) NOT NULL,
                role VARCHAR(15) NOT NULL,
                date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        
    def insert_data_products(self, data):
        """inserts values into table products"""

        try:
            self.cursor.execute(
                """
                INSERT INTO products(product_name, category, unit_price, quantity, measure) \
                VALUES('{}', '{}', {}, {}, '{}')""".format(data.product_name, data.category, 
                data.unit_price, data.quantity, data.measure)
            )
        except:
            return False

    def check_product_exists_name(self, product_name):
        """check if product exists"""

        try:
            self.cursor.execute(
                "SELECT * FROM products WHERE product_name = '{}' AND delete_status = FALSE" .format(product_name)
            )
            return self.cursor.fetchone()
        except:
            return False

    def getProducts(self):
        """get all products"""

        try:
            self.cursor.execute(
                "SELECT * FROM products WHERE delete_status = FALSE"
            )
            _products = self.cursor.fetchall()
            for product in _products:
                return ("products: {0}".format(product))

        except:
            return False

    def getoneProduct(self, _pid):
        """get one product"""

        try:
            self.cursor.execute(
                "SELECT * FROM products WHERE product_id = %s AND delete_status = FALSE", [_pid]
            )
            _products = self.cursor.fetchall()

            if _products:
                for products in _products:
                    return ("product: {0}".format(products)) 
            else:
                return ("no product with that id")

        except:
            return False

    def deloneProduct(self, _pid):
        """delete one product"""
        try:
            self.cursor.execute(
                # "DELETE FROM products WHERE product_id = %s", [_pid]
                "UPDATE products SET delete_status=TRUE , date_modified =CURRENT_TIMESTAMP WHERE product_id = {}".format(_pid
                )
            )
        except:
            return False

    def check_product_exists_id(self, product_id):
        """check if product exists"""

        try:
            self.cursor.execute(
                "SELECT * FROM products WHERE product_id = %s AND delete_status= FALSE", [product_id]) 
            return self.cursor.fetchone()

        except:
            return False

    def modify_product(self, product_name, category, unit_price, quantity, measure,product_id):
        """modify product"""
        try:
            self.cursor.execute(
                "UPDATE products SET product_name='{}', category='{}', \
                unit_price={}, quantity={}, measure = '{}', date_modified=CURRENT_TIMESTAMP\
                WHERE product_id = {} AND delete_status = FALSE"
                .format(product_name, category, unit_price, quantity, measure, product_id)
            )

        except:
            return False
    
    def insert_table_users(self, record):
        """add data to table users"""

        try:
            self.cursor.execute(
                """
                INSERT INTO users(name, user_name, password, role) \
                VALUES('{}', '{}', '{}', '{}')
                """.format(record.name, record.user_name, record.password, record.role)
            )
        
        except:
            return False

    def default_admin(self):
        """inserts default admin"""

        try:
            self.cursor.execute(
                """
                INSERT INTO users(name, user_name, password, role)\
                VALUES('Vicki', 'vickib', 'vibel', 'admin');
                """
            )
        
        except:
            return False

    def insert_table_login(self, record):
        """add data to table login"""

        try:
            self.cursor.execute(
                """
                INSERT INTO login(user_name, password, role) \
                VALUES('{}', '{}', '{}')
                """.format(record.user_name, record.password, record.role)
            )
        
        except:
            return False

    def getUsers(self):
        """get all users"""
        try:
            self.cursor.execute(
                "SELECT * FROM users WHERE delete_status= FALSE"
            )
            _users = self.cursor.fetchall()
            for user in _users:
                return ("users: {0}" .format(user))
        except:
            return False

    def check_user_exists(self, user_name, password, role):
        """check if user exists"""

        try:
            self.cursor.execute(
                "SELECT * FROM users WHERE user_name = '{}' AND password = '{}' AND role = '{}' AND delete_status= FALSE" .format(user_name, password, role)
            )
            return self.cursor.fetchone()
        
        except:
            return False

    def getoneUser(self, _uid):
        """get one user"""

        try:
            self.cursor.execute(
                "SELECT * FROM users WHERE user_id = %s AND delete_status= FALSE", [_uid]
            )
            _users = self.cursor.fetchall()
            if _users:
                for user in _users:
                    return ("user: {0}".format(user)) 
            else:
                return ("no user with that id")

        except:
            return False

    def deloneuser(self, _uid):
        """delete one user"""

        try:
            self.cursor.execute(
                # "DELETE FROM users WHERE user_id = %s", [_uid]
                "UPDATE users SET delete_status=TRUE, date_modified= CURRENT_TIMESTAMP WHERE user_id = {}".format(_uid)
            )
        except:
            return False

    def check_user_exists_id(self, user_id):
        """check if user exists"""

        try:
            self.cursor.execute(
                "SELECT * FROM users WHERE user_id = %s AND delete_status= FALSE", [user_id]) 
            return self.cursor.fetchone()

        except:
            return False

    def insert_data_sales(self, data):
        """insert data into sales table"""

        try:
            self.cursor.execute("INSERT INTO sales(user_id) VALUES({}) RETURNING sale_id".format(data.user_id)
            )
            return self.cursor.fetchone()[0]
        
        except:
            return False

    def insert_data_sales_has_products(self, data):
        """insert data into salesproducts table"""

        try:
            self.cursor.execute(
                """
                INSERT INTO sales_has_products(sale_id, product_id, quantity, total) \
                VALUES({}, {}, {}, {})
                """.format(data.sale_id, data.product_id, data.quantity, data.total)
            )
        
        except:
            return False
        
    def getsales(self):
        """get one sale"""

        try:
            self.cursor.execute(
                "SELECT sales.sale_id, sales.user_id, products.product_id, \
                sales_has_products.total, sales_has_products.quantity, sales.date_created, sales.date_modified \
                FROM sales_has_products, sales, products WHERE sales.sale_id = sales_has_products.sale_id \
                AND products.product_id = sales_has_products.product_id" 
            )
            _sale = self.cursor.fetchall()
            for sale in _sale:
                return ("sales: {0}" .format(sale))
        
        except:
            return False

    def getQuantity(self, id_):
        """get qty"""

        try:
            self.cursor.execute(
                "SELECT quantity FROM products WHERE product_id = %s AND delete_status= FALSE", [id_]
            )
            return self.cursor.fetchone()[0]
        
        except:
            return False

    def getPrice(self, id_):
        """get price"""

        try:
            self.cursor.execute(
                "SELECT unit_price FROM products WHERE product_id = %s AND delete_status= FALSE", [id_]
            )
            return self.cursor.fetchone()[0]
        
        except:
            return False

    def updateProductqty(self, qty, pdtid):
        """update pdt qty"""

        try:
            self.cursor.execute(
                "UPDATE products SET quantity={}, date_modified=CURRENT_TIMESTAMP WHERE product_id = {} \
                AND delete_status=False".format(qty, pdtid)
            )
        
        except:
            return False
