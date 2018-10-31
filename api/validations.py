"""validations class"""
from flask import jsonify
from database import DatabaseConnection

db = DatabaseConnection()

"""define my validation methods"""

def validate_add_product(**kwargs):
        _productname_ = kwargs.get("product_name")
        _category_ = kwargs.get("category")
        _unitprice_ = kwargs.get("unit_price")
        _quantity_ = kwargs.get("quantity")
        _measure_ = kwargs.get("measure")
    
        # check empty fails
        if not _productname_ or not _category_ or not _unitprice_ or not _quantity_ or not _measure_:
            return jsonify({"error": "fields should not be empty"}), 400
        #check if unitprice and quantity are integers
        if not isinstance(_unitprice_, int) or not isinstance(_quantity_):
            return jsonify({"error": "unit price and quantity have to be integers"}), 400
        # check if product name exists
        data_product_name_exist = db.check_product_exists_name(_productname_)
        if data_product_name_exist:
            return jsonify({'message': "Product already exists"}), 400

    

