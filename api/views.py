"""!Flask web api for Store Manager"""
from flask import Flask, jsonify, abort, request
import datetime
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from werkzeug.security import check_password_hash, generate_password_hash
from database import DatabaseConnection
from models import Products, Sales, Users, Login, SalesHasProducts
from validations import (validate_product, validate_user_signup, validate_user_login, validate_sales)

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)

database = DatabaseConnection()
database.drop_tables()
database.create_tables()
database.default_admin()

 #error handlers
@app.errorhandler(404)
def not_found(self, error):
    """ not_found(error) -returns error not found"""
    return jsonify({'error': 'NOT FOUND'}), 404

@app.errorhandler(400)
def bad_request(self, error):
    """ bad_request(error) -returns error bad request"""
    return jsonify({'error': 'BAD REQUEST'}), 400

@app.errorhandler(405)
def mtd_not_allowed(self, error):
    """ mtd_not_allowed(error) -returns error method not allowed"""
    return jsonify({'error': "METHOD NOT ALLOWED"}), 405

@app.errorhandler(401)
def unauthorized(self, error):
    """ unauthorized(error) -returns error unauthorized"""
    return jsonify({'error': "NOT AUTHORIZED"}), 401

@app.route('/')
def hello():
    """my home"""
    return "Hello Welcome to Store Manager API"

@app.route('/api/v1/products', methods=['GET', 'POST'])
def products():
    """returns all products"""
    if request.method == 'GET':
        productget = database.getProducts()
        if productget:
            return jsonify({'products': productget}), 200
        else:
            return jsonify({'message': "There are no products"}), 404
  
    elif request.method == 'POST':
        """returns a product that has been added"""
        data = request.get_json()
        prod_name = data.get('product_name')
        prod_cat = data.get('category')
        prod_price = data.get('unit_price')
        prod_qty = data.get('quantity')
        prod_meas = data.get('measure')
            
        valprod = validate_product(product_name=prod_name, 
                                   category=prod_cat, 
                                   unit_price=prod_price, 
                                   quantity=prod_qty, 
                                   measure=prod_meas)
        if valprod:
            return valprod
        else:
            obj_products = Products(prod_name, prod_cat, prod_price, prod_qty, prod_meas)
            database.insert_data_products(obj_products)
            return jsonify({"Success": "product has been added"}), 201
    else:
        abort(405)

# get specific product and delete a product and modify product
@app.route('/api/v1/products/<int:_id>', methods=['GET','DELETE', 'PUT'])
@jwt_required
def _product_(_id):
    current_user = get_jwt_identity()
    if request.method == 'GET':
        """returns a product via its id"""
        if current_user == 'admin' or current_user == 'attendant':
            _product_ = database.getoneProduct(_id)
            if _product_:
                return jsonify({'product': _product_}), 200
            else:
                return jsonify({'product': "product has not been found"}), 404
        else:
            return jsonify({'message': "You are not authorized"}), 401
    elif request.method == 'DELETE':
        """delete_product(_id)--deletes product"""
        if current_user == 'admin':
            del_prod = database.check_product_exists_id(_id)
            if not del_prod:
                return jsonify({"error": "Product your are trying to delete does not exist"}), 404
            else:
                database.deloneProduct(_id)
                return jsonify({"message": "Product has been deleted successfully"}), 200
        else:
            return jsonify({'message': "You are unauthorized"}), 401
    elif request.method == 'PUT':
        """put product"""
        if current_user == 'admin':
            prod = database.check_product_exists_id(_id)
            if not prod:
                return jsonify({"error": "product you are trying to modify does not exist"}), 404
            else:
                data = data = request.get_json()
                prod_name = data.get('product_name')
                prod_cat = data.get('category')
                prod_price = data.get('unit_price')
                prod_qty = data.get('quantity')
                prod_meas = data.get('measure')

                valprod = validate_product(product_name=prod_name, 
                                           category=prod_cat, 
                                           unit_price=prod_price, 
                                           quantity=prod_qty, 
                                           measure=prod_meas)
                if valprod:
                    return valprod
                else:
                    database.modify_product(prod_name, prod_cat, prod_price, prod_qty, prod_meas, _id)
                    return jsonify({"Success": "product has been modified"}), 201
        else:
            return jsonify({"message": "You are not authorized"}), 401
    else:
        abort(405)  

#get users
@app.route('/api/v1/users', methods=['GET'])
@jwt_required
def _users_():
    """returns all users"""
    current_user = get_jwt_identity()
    if current_user == 'admin':
        if request.method == 'GET':
            userget = database.getUsers()
            if userget:
                return jsonify({'users': userget}), 200
            else:
                return jsonify({'message': "There are no users"}), 404
    else:
        return jsonify({"message": "You are not authorized"}), 401

# create user auth
@app.route('/api/v1/auth/signup', methods=['POST'])
@jwt_required
def signup():
    """returns a user that has been added"""
    current_user = get_jwt_identity()
    if current_user == 'admin':
        if request.method == 'POST':
            data = request.get_json()
            name = data.get('name')
            user_name = data.get('user_name')
            password = data.get('password')
            role = data.get('role')

            valuser = validate_user_signup(name=name, user_name = user_name, password=password, role = role)
            if valuser:
                return valuser
            else:
                obj_users = Users(name, user_name, password, role)
                database.insert_table_users(obj_users)
                return jsonify({"Success": "user has been added"}), 201
        else:
            return jsonify({"message": "Method not allowed"}), 405
    else:
        return jsonify({"message": "You are not authorized"}), 401
# user login
# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose
@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    if request.method == 'POST':
        """returns a user login"""
        data = request.get_json()
        user_name = data.get('user_name')
        password = data.get('password')
        role = data.get('role')

        loguserval = validate_user_login(user_name = user_name, password=password, role = role)
        if loguserval:
            return loguserval
        else:
            # Identity can be any data that is json serializable
            obj_login = Login(user_name, password, role)
            database.insert_table_login(obj_login)
            access_token = create_access_token(identity=role, expires_delta=datetime.timedelta(days=100))
            return jsonify(access_token="Bearer {}".format(access_token)), 200
    else:
        abort(405)

#delete modify users
# get specific product and delete a product and modify product
@app.route('/api/v1/users/<int:_id>', methods=['GET','DELETE'])
@jwt_required
def _user_(_id):
    current_user = get_jwt_identity()
    if request.method == 'GET':
        """returns a user via its id"""
        if current_user == 'admin':
            _user_ = database.getoneUser(_id)
            if _user_:
                return jsonify({'user': _user_}), 200
            else:
                return jsonify({'user': "user has not been found"}), 404
        else:
            return jsonify({"message": "You are not authorized"}), 401
    elif request.method == 'DELETE':
        """delete_user(_id)--deletes user"""
        if current_user == 'admin':
            del_user = database.check_user_exists_id(_id)
            if not del_user:
                return jsonify({"error": "user your are trying to delete does not exist"}), 404
            else:
                database.deloneuser(_id)
                return jsonify({"message": "user has been deleted successfully"}), 200
        else:
            return jsonify({"message": "You are not authorized"}), 401
    else:
        abort(405)  

#add a sale
@app.route('/api/v1/sales', methods=['GET','POST'])
@jwt_required
def _sale():
    """_sale() """
    current_user = get_jwt_identity()
    if request.method == 'GET':
        if current_user == 'admin' or current_user == 'attendant':
            saleget = database.getsales()
            if saleget:
                return jsonify({'sales': saleget}), 200
            else:
                return jsonify({'message': "There are no sales"}), 404
        else:
            return jsonify({"message": "You are not authorized"}), 401
    elif request.method == 'POST':
        """add sales"""
        if current_user == 'attendant':
            data = request.get_json()
            user_id = int(data.get('user_id'))
            quantity = int(data.get('quantity'))
            product_id = int(data.get('product_id'))

            # check empty fields
            valsale=validate_sales(user_id=user_id,product_id=product_id,quantity=quantity)
            if valsale:
                return valsale
            else:
                # insert into sales tab;e
                obj_sales = Sales(user_id)
                saleid = database.insert_data_sales(obj_sales)
                # get quantity
                getQty = int(database.getQuantity(product_id))
                if quantity > getQty:
                    return jsonify({"error": "The product's quantity is not enough for you to make sale"}), 400
                else:
                    # get unit price
                    getPrice = int(database.getPrice(product_id))
                    # calculate total
                    total = quantity * getPrice
                    # new qty
                    newqty = getQty - quantity
                    #insert into sale has products table
                    obj_salepdt = SalesHasProducts(saleid, product_id, quantity, total)
                    database.insert_data_sales_has_products(obj_salepdt)
                    #update products table
                    database.updateProductqty(newqty, product_id)
                    return jsonify({"Success": "sale has been added"}), 201
        else:
            return jsonify({"message": "You are not authorized"}), 401
    else:
        abort(405)

if __name__ == '__main__':
    app.run(debug=True)
