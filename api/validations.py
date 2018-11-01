"""validations class"""
from flask import jsonify
from api.database import DatabaseConnection

db = DatabaseConnection()

"""define my validation methods"""

def validate_product(**kwargs):
        _productname_ = kwargs.get("product_name")
        _category_ = kwargs.get("category")
        _unitprice_ = kwargs.get("unit_price")
        _quantity_ = kwargs.get("quantity")
        _measure_ = kwargs.get("measure")
    
        # check empty fields
        if not _productname_ or not _category_ or not _unitprice_ or not _quantity_ or not _measure_:
            return jsonify({"error": "fields should not be empty"}), 400
        #check if unitprice and quantity are integers
        if not isinstance(_unitprice_, int) or not isinstance(_quantity_, int):
            return jsonify({"error": "unit price and quantity have to be integers"}), 400
        # check if product name exists
        data_product_name_exist = db.check_product_exists_name(_productname_)
        if data_product_name_exist:
            return jsonify({'message': "Product already exists"}), 400

def validate_user_signup(**kwargs):
    name = kwargs.get("name")
    user_name = kwargs.get("user_name")
    password = kwargs.get("password")
    role = kwargs.get("role")

    #check empty fields
    if not name or not user_name or not password or not role:
        return jsonify({"error": "fields should not be empty"}), 400

    # check if user exists
    data_user_exist = db.check_user_exists(user_name, password, role)
    if data_user_exist:
        return jsonify({'error': "user with that username already exists"}), 400

def validate_user_login(**kwargs):
    user_name = kwargs.get("user_name")
    password = kwargs.get("password")
    role = kwargs.get("role")

    #check empty fields
    if not user_name or not password or not role:
        return jsonify({"error": "fields should not be empty"}), 400
    
    data_user_exist = db.check_user_exists(user_name, password, role)
    if not data_user_exist:
        return jsonify({'error': "user with that username, password, role doesn't exist"}), 400
    
def validate_sales(**kwargs):
    """validate sales"""
    user_id = kwargs.get("user_id")
    product_id = kwargs.get("product_id")
    quantity = kwargs.get("quantity")

    if not user_id:
        return jsonify({'message': "Field can't be empty"}), 400

    if type(user_id) is not int:
        return jsonify({'message': "field have to be integers"}), 400
    
    if not quantity or not product_id:
        return jsonify({'message': "Fields can't be empty"}), 400

    if type(product_id) is not int or type(quantity) is not int:
        return jsonify({'message': "fields have to be integers"}), 400

    #check if product exists
    product = db.getoneProduct(product_id)
    if not product:
        return jsonify({"error": "This product doesn't exist"}), 404

    # check if user exists
    user = db.getoneUser(user_id)
    if not user:
        return jsonify({"error": "This user doesn't exist"}), 404
    data_user_exist = db.check_user_exists_id(user_id)
    if not data_user_exist:
        return jsonify({'error': "user does not exist"}), 400

    

    
    

