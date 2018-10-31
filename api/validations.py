"""validations class"""
from flask import jsonify
from database import DatabaseConnection

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
    data_user_name_exist = db.check_user_exists_name(user_name)
    data_user_pass_exist = db.check_user_exists_password(password)

    if data_user_name_exist:
        return jsonify({'error': "user name already exists"}), 400
    if data_user_pass_exist:
        return jsonify({'error': "try another password-that one may have been used"}), 400

def validate_user_login(**kwargs):
    user_name = kwargs.get("user_name")
    password = kwargs.get("password")
    role = kwargs.get("role")

    #check empty fields
    if not user_name or not password or not role:
        return jsonify({"error": "fields should not be empty"}), 400
    
    data_user_name_exist = db.check_user_exists_name(user_name)
    data_user_pass_exist = db.check_user_exists_password(password)
    data_user_role_exist = db.check_user_exists_role(role, user_name)

    if not data_user_name_exist:
        return jsonify({'error': "user name does not exist, sign up first"}), 400
    if not data_user_pass_exist:
        return jsonify({'error': "invalid password"}), 400
    if not data_user_role_exist:
        return jsonify({'error': "invalid role"}), 400
def validate_sales(**kwargs):
    """validate sales"""
