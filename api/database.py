"""Database models"""
from flask import Flask, jsonify
import psycopg2
from models import Products, Sales, Users, SalesHasProducts, Login

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
    def drop_tables(self):
        """drop tables if exist"""
        self.cursor.execute(
            "DROP TABLE IF EXISTS products, users, sales, saleshasproducts, login CASCADE"
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
                date DATE DEFAULT CURRENT_DATE,
                status_delete BOOLEAN DEFAULT FALSE);
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
                date DATE DEFAULT CURRENT_DATE,
                status_delete BOOLEAN DEFAULT FALSE);
            """
        )
        """create sales table"""  
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sales (
                sale_id SERIAL PRIMARY KEY,  
                user_id integer NOT NULL,
                date DATE DEFAULT CURRENT_DATE,
                status_delete BOOLEAN DEFAULT FALSE,
                CONSTRAINT userid_foreign FOREIGN KEY (user_id) 
                    REFERENCES users(user_id) 
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
                status_delete BOOLEAN DEFAULT FALSE,
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
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        
    def insert_data_products(self, data):
        """inserts values into table products"""
        try:
            self.cursor.execute(
                """
                INSERT INTO products(product_name, category, unit_price, quantity, measure) \
                VALUES('{}', '{}', {}, {}, '{}')""".format(data.product_name, data.category, data.unit_price, data.quantity, data.measure)
            )
        except:
            return False
    def check_product_exists_name(self, product_name):
        """check if product exists"""
        try:
            self.cursor.execute(
                "SELECT * FROM products WHERE product_name = '{}' AND status_delete = FALSE" .format(product_name)
            )
            return self.cursor.fetchone()
        except:
            return False
    def getProducts(self):
        """get all products"""
        try:
            self.cursor.execute(
                "SELECT * FROM products WHERE status_delete = FALSE"
            )
            _products = self.cursor.fetchall()
            return _products 
        except:
            return False
    def getoneProduct(self, _pid):
        """get one product"""
        try:
            self.cursor.execute(
                "SELECT * FROM products WHERE product_id = %s AND status_delete = FALSE", [_pid]
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
        self.cursor.execute(
            # "DELETE FROM products WHERE product_id = %s", [_pid]
            "UPDATE products SET status_delete=TRUE WHERE product_id = %s", [_pid]
        )
    def check_product_exists_id(self, product_id):
        """check if product exists"""
        self.cursor.execute(
            "SELECT * FROM products WHERE product_id = %s AND status_delete= FALSE", [product_id]) 
        return self.cursor.fetchone()  
    def modify_product(self, product_name, category, unit_price, quantity, measure, product_id):
        """modify product"""
        self.cursor.execute(
            "UPDATE products SET product_name='{}', category='{}', unit_price={}, quantity={}, measure = '{}' WHERE product_id = {} status_delete = FALSE"
            .format(product_name, category, unit_price, quantity, measure, product_id)
        ) 
    
    def insert_table_users(self, record):
        """add data to table users"""
        self.cursor.execute(
            """
            INSERT INTO users(name, user_name, password, role) \
            VALUES('{}', '{}', '{}', '{}')
            """.format(record.name, record.user_name, record.password, record.role)
        )
    def default_admin(self):
        """inserts default admin"""
        self.cursor.execute(
            """
            INSERT INTO users(name, user_name, password, role)\
            VALUES('Vicki', 'vickib', 'vibel', 'admin');
            """
        )
    def insert_table_login(self, record):
        """add data to table login"""
        self.cursor.execute(
            """
            INSERT INTO login(user_name, password, role) \
            VALUES('{}', '{}', '{}')
            """.format(record.user_name, record.password, record.role)
        )
    def getUsers(self):
        """get all users"""
        self.cursor.execute(
            "SELECT * FROM users WHERE status_delete= FALSE"
        )
        _users = self.cursor.fetchall()
        return _users 
    def check_user_exists_name(self, user_name):
        """check if user exists"""
        self.cursor.execute(
            "SELECT * FROM users WHERE user_name = '{}' AND status_delete= FALSE" .format(user_name)
        )
        return self.cursor.fetchone()
    def check_user_exists_role(self, role, user_name):
        """check if role exists"""
        self.cursor.execute(
            "SELECT * FROM users WHERE role = '{}' AND user_name='{}' AND status_delete= FALSE" .format(role, user_name)
        )
        return self.cursor.fetchone()
    def check_user_exists_password(self, password):
        """check if user exists"""
        self.cursor.execute(
            "SELECT * FROM users WHERE password = '{}' AND status_delete= FALSE" .format(password)
        )
        return self.cursor.fetchone()
    def getoneUser(self, _uid):
        """get one user"""
        self.cursor.execute(
            "SELECT * FROM users WHERE user_id = %s AND status_delete= FALSE", [_uid]
        )
        _users = self.cursor.fetchall()
        if _users:
            for user in _users:
                return ("user: {0}".format(user)) 
        else:
            return ("no user with that id")
    def deloneuser(self, _uid):
        """delete one user"""
        self.cursor.execute(
            # "DELETE FROM users WHERE user_id = %s", [_uid]
            "UPDATE users SET status_delete=TRUE WHERE user_id = %s", [_uid]
        )
    def check_user_exists_id(self, user_id):
        """check if user exists"""
        self.cursor.execute(
            "SELECT * FROM users WHERE user_id = %s AND status_delete= FALSE", [user_id]) 
        return self.cursor.fetchone()  
    def modify_user(self, name, user_name, password, role, user_id):
        """modify user"""
        self.cursor.execute(
            "UPDATE users SET name='{}', user_name='{}', password='{}', role='{}' WHERE user_id = {}"
            .format(name, user_name, password, role, user_id)
        ) 
    def insert_data_sales(self, data):
        """insert data into sales table"""
        self.cursor.execute(
            """
            INSERT INTO sales(user_id) \
            VALUES({})
            """.format(data.user_id)
        )
        
    def insert_data_saleshasproducts(self, data):
        """insert data into salesproducts table"""
        self.cursor.execute(
            """
            INSERT INTO saleshasproducts(product_id, quantity, total) \
            VALUES({}, {}, {})
            """.format(data.product_id, data.quantity, data.total)
        )
    def getsales(self):
        """get one sale"""
        self.cursor.execute(
            "SELECT sales.sale_id, sales.user_id, products.product_id, \
            saleshasproducts.total, saleshasproducts.quantity, sales.date \
            FROM saleshasproducts WHERE status_delete= FALSE INNER JOIN sales ON sales.sale_id = saleshasproducts.sale_id \
            INNER JOIN products ON products.product_id = saleshasproducts.product_id" 
        )
        _sale = self.cursor.fetchall()
        return _sale
    def getQuantity(self, id_):
        """get qty"""
        self.cursor.execute(
            "SELECT quantity FROM products WHERE product_id = %s AND status_delete= FALSE", [id_]
        )
        return self.cursor.fetchone()
    def getPrice(self, id_):
        """get price"""
        self.cursor.execute(
            "SELECT unit_price FROM products WHERE product_id = %s AND status_delete= FALSE", [id_]
        )
        return self.cursor.fetchone()
    def getSaleId(self, id_):
        """get sale"""
        self.cursor.execute(
            "SELECT sale_id FROM sales WHERE sale_id = %s AND status_delete= FALSE", [id_]
        )
        return self.cursor.fetchone()
    def updateProductqty(self, qty, pdtid):
        """update pdt qty"""
        self.cursor.execute(
            "UPDATE products SET quantity={} WHERE product_id = {} AND status_delete=False".format(qty, pdtid)
        )
