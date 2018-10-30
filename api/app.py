"""!Flask web api for Store Manager"""
from flask import Flask, jsonify, abort, make_response, request
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from models import DatabaseConnection
from db import Products, Sales, Users, Login, SalesHasProducts

database = DatabaseConnection()
database.drop_tables()
database.create_tables()

app = Flask(__name__)
"""initializing"""

#error handlers
@app.errorhandler(404)
def not_found(error):
    """ not_found(error) -returns error not found"""
    return make_response(jsonify({'error': 'NOT FOUND'}), 404)

@app.errorhandler(400)
def bad_request(error):
    """ bad_request(error) -returns error bad request"""
    return make_response(jsonify({'error': 'BAD REQUEST'}), 400)

@app.errorhandler(405)
def mtd_not_allowed(error):
    """ mtd_not_allowed(error) -returns error method not allowed"""
    return make_response(jsonify({'error': "METHOD NOT ALLOWED"}), 405)

@app.route('/')
def hello():
    """my first home"""
    return "Hello Welcome to Store Manager API"

# #other methods
# def _get_product(productid):
#     """_get_product(productid) returns a product in products via product_id"""
#     # return [product for product in PRODUCTS if product['product_id'] == productid]

#get all products and post a product
@app.route('/api/v1/products', methods=['GET', 'POST'])
def products():
    """returns all products"""
    if request.method == 'GET':
        productget = database.getProducts()
        if productget:
            return jsonify({'products': productget}), 200
        else:
            return jsonify({'message': "There are no products"}), 404
  
    if request.method == 'POST':

        """returns a product that has been added"""
        data = request.get_json()
        prod_name = data.get('product_name')
        prod_cat = data.get('category')
        prod_price = data.get('unit_price')
        prod_qty = data.get('quantity')
        prod_meas = data.get('measure')
        

        # check if product exists
        data_product_name_exist = database.check_product_exists_name(prod_name)

        if not prod_name or not prod_cat or not prod_price or not prod_qty or not prod_meas:
            return jsonify({'message': "Fields can't be empty"}), 400
        elif not isinstance(prod_price, int) or not isinstance(prod_qty, int):
            return jsonify({'message': "Price and Quantity have to be integers"}), 400
        elif data_product_name_exist:
            return jsonify({'message': "Product already exists"}), 400
        else:
            obj_products = Products(prod_name, prod_cat, prod_price, prod_qty, prod_meas)
            database.insert_data_products(obj_products)
            return jsonify({"Success": "product has been added"}), 201
    else:
        abort(405)

# get specific product and delete a product and modify product
@app.route('/api/v1/products/<int:_id>', methods=['GET','DELETE', 'PUT'])
def _product_(_id):
    if request.method == 'GET':
        """returns a product via its id"""
        _product_ = database.getoneProduct(_id)
        if _product_:
            return jsonify({'product': _product_}), 200
        else:
            return jsonify({'product': "product has not been found"}), 404
    elif request.method == 'DELETE':
        """delete_product(_id)--deletes product"""
        del_prod = database.check_product_exists_id(_id)
        if not del_prod:
            return jsonify({"error": "Product your are trying to delete does not exist"}), 404
        else:
            database.deloneProduct(_id)
            return jsonify({"message": "Product has been deleted successfully"}), 200  
    elif request.method == 'PUT':
        """put product"""
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

            if not prod_name or not prod_cat or not prod_price or not prod_qty or not prod_meas:
                return jsonify({'message': "Fields can't be empty"}), 400
            elif not isinstance(prod_price, int) or not isinstance(prod_qty, int):
                return jsonify({'message': "Price and Quantity have to be integers"}), 400
            else:
                database.modify_product(prod_name, prod_cat, prod_price, prod_qty, prod_meas, _id)
                return jsonify({"Success": "product has been modified"}), 201
    else:
        abort(405)  

#get users
@app.route('/api/v1/users', methods=['GET'])
def _users_():
    """returns all users"""
    if request.method == 'GET':
        userget = database.getUsers()
        if userget:
            return jsonify({'users': userget}), 200
        else:
            return jsonify({'message': "There are no users"}), 404

# create user auth
@app.route('/api/v1/auth/signup', methods=['POST'])
def signup():
        """returns a user that has been added"""
        data = request.get_json()
        name = data.get('name')
        user_name = data.get('user_name')
        password = data.get('password')
        role = data.get('role')
        # check if user exists
        data_user_name_exist = database.check_user_exists_name(user_name)
        data_user_pass_exist = database.check_user_exists_password(password)
        if not name or not user_name or not password or not role:
            return jsonify({'message': "Fields can't be empty"}), 400
        elif data_user_name_exist:
            return jsonify({'error': "user name already exists"}), 400
        elif data_user_pass_exist:
            return jsonify({'error': "try another password-that one may have been used"}), 400
        else:
            obj_users = Users(name, user_name, password, role)
            database.insert_table_users(obj_users)
            return jsonify({"Success": "user has been added"}), 201
# user login
@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    if request.method == 'POST':
        """returns a user login"""
        data = request.get_json()
        user_name = data.get('user_name')
        password = data.get('password')

        if not user_name or not password:
            return jsonify({'message': "Fields can't be empty"}), 400
        else:
            obj_login = Login(user_name, password)
            database.insert_table_login(obj_login)
            return jsonify({"Success": "user has been logged in"}), 201
    else:
        abort(405)

#delete modify users
# get specific product and delete a product and modify product
@app.route('/api/v1/users/<int:_id>', methods=['GET','DELETE', 'PUT'])
def _user_(_id):
    if request.method == 'GET':
        """returns a user via its id"""
        _user_ = database.getoneUser(_id)
        if _user_:
            return jsonify({'user': _user_}), 200
        else:
            return jsonify({'user': "user has not been found"}), 404
    elif request.method == 'DELETE':
        """delete_user(_id)--deletes user"""
        del_user = database.check_user_exists_id(_id)
        if not del_user:
            return jsonify({"error": "user your are trying to delete does not exist"}), 404
        else:
            database.deloneuser(_id)
            return jsonify({"message": "user has been deleted successfully"}), 200
    elif request.method == 'PUT':
        """put user"""
        u = database.check_user_exists_id(_id)
        if not u:
            return jsonify({"error": "user you are trying to modify does not exist"}), 404
        else:
            data = data = request.get_json()
            name = data.get('name')
            user_name = data.get('user_name')
            password = data.get('password')
            role = data.get('role')

            if not name or not user_name or not password or not role:
                return jsonify({'message': "Fields can't be empty"}), 400
            else:
                database.modify_user(name, user_name, password, role, _id)
                return jsonify({"Success": "user has been modified"}), 201
    else:
        abort(405)  

#add a sale
@app.route('/api/v1/sales', methods=['GET','POST'])
def _sale():
    """_sale() """
    if request.method == 'GET':
        saleget = database.getsales()
        if saleget:
            return jsonify({'sales': saleget}), 200
        else:
            return jsonify({'message': "There are no sales"}), 404
    elif request.method == 'POST':
        """add sales"""
        data = request.get_json()
        user_id = data.get('user_id')
        quantity = data.get('quantity')
        product_id = data.get('product_id')

        # get quantity
        getQty = database.getQuantity(product_id)
        # get unit price
        getPrice = database.getPrice(product_id)
        # calculate total
        total = quantity * getPrice
        # check empty fields
        if not data or not user_id or not quantity or not product_id or not total:
            return jsonify({'message': "Fields can't be empty"}), 400
        # validate integers
        elif not isinstance(user_id, int) or not isinstance(quantity, int) or not isinstance(product_id, int) or not isinstance(total, int):
            return jsonify({'message': "fields have to be integers"}), 400
        else:
            obj_sales = Sales(user_id)
            database.insert_data_sales(obj_sales)
            obj_salepdt = SalesHasProducts(product_id, quantity, total)
            database.insert_data_saleshasproducts(obj_salepdt)
            return jsonify({"Success": "user has been added"}), 201
    else:
        abort(405)

#     data = request.get_json()
#     prod_id = data.get('product_id')
#     prod_quantity = data.get('quantity')
#     if not prod_id or not prod_quantity:
#         return jsonify({'message': "Fields can't be empty"}), 400
#     elif not isinstance(prod_id, int) and not isinstance(prod_quantity, int):
#         return jsonify({'message': "Id and Quantity have to be integers"}), 400
#     else:
#         for product in PRODUCTS:
#             if prod_id == product['product_id']:
#                 _quantity_ = product['quantity'] - int(prod_quantity)
#                 product['quantity'] = _quantity_
                
#                 _sale = {
#                     'sale_id':SALES[-1]['sale_id'] + 1,
#                     'product_id':prod_id,
#                     'quantity': prod_quantity
#                 }
#                 SALES.append(_sale)
#                 return jsonify({"Success":"sale '{0}' added".format(_sale["sale_id"])}), 201

# #get all sales
# @app.route('/api/v1/sales', methods=['GET'])
# def get_sales():
#     """get_sales() -- returns all sales"""
#     if SALES:
#         return jsonify({'sales': SALES})
#     else:
#         return jsonify({'message': "There are no sale records"})

if __name__ == '__main__':
    app.run(debug=True)
