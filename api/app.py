"""!Flask web api for Store Manager"""
from flask import Flask, jsonify, abort, make_response, request
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from models import DatabaseConnection
from db import Products, Sales, Users

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

#other methods
def _get_product(productid):
    """_get_product(productid) returns a product in products via product_id"""
    return [product for product in PRODUCTS if product['product_id'] == productid]

#get all products and post a product
@app.route('/api/v1/products', methods=['GET', 'POST'])
def products():
    """returns all products"""
    if request.method == 'GET':
        if PRODUCTS:
            return jsonify({'products': PRODUCTS})
        else:
            return jsonify({'message': "There are no products"})
    elif request.method == 'POST':

        """returns a product that has been added"""
        data = request.get_json()
        prod_name = data.get('product_name')
        prod_cat = data.get('category')
        prod_price = data.get('unit_price')
        prod_qty = data.get('quantity')
        prod_meas = data.get('measure')

        if not prod_name or not prod_cat or not prod_price or not prod_qty or not prod_meas:
            return jsonify({'message': "Fields can't be empty"}), 400
        elif not isinstance(prod_price, int) or not isinstance(prod_qty, int):
            return jsonify({'message': "Price and Quantity have to be integers"}), 400
        # elif prod_name is not productname:
        #      return jsonify({'message': "Product already exists"}), 400
        else:
            obj_products = Products(prod_name, prod_cat, prod_price, prod_qty, prod_meas)
            databaseConnect = DatabaseConnection()
            databaseConnect.insert_data(obj_products)
            # PRODUCTS.append(_product)
            return jsonify({"Success":"product '{0}' added".format(_product["product_id"])}), 201
    else:
        abort(405)

#get specific product and delete a product
@app.route('/api/v1/products/<int:_id>', methods=['GET','DELETE'])
def _product_(_id):
    if request.method == 'GET':
        """returns a product via its id"""
        _product_ = _get_product(_id)
        if _product_:
            return jsonify({'product': _product_})
        else:
            abort(404)         
    elif request.method == 'DELETE':
        """delete_product(_id)--deletes product"""
        prod_ = _get_product(_id)
        if prod_:
            PRODUCTS.remove(prod_[0])
            return jsonify({'product': "product has been deleted"})
        else:
            abort(404)
    else:
        abort(405)  

#add a sale
@app.route('/api/v1/sales', methods=['POST'])
def create_sale():
    """create_sale() --returns a product that has been added"""
    data = request.get_json()
    prod_id = data.get('product_id')
    prod_quantity = data.get('quantity')
    if not prod_id or not prod_quantity:
        return jsonify({'message': "Fields can't be empty"}), 400
    elif not isinstance(prod_id, int) and not isinstance(prod_quantity, int):
        return jsonify({'message': "Id and Quantity have to be integers"}), 400
    else:
        for product in PRODUCTS:
            if prod_id == product['product_id']:
                _quantity_ = product['quantity'] - int(prod_quantity)
                product['quantity'] = _quantity_
                
                _sale = {
                    'sale_id':SALES[-1]['sale_id'] + 1,
                    'product_id':prod_id,
                    'quantity': prod_quantity
                }
                SALES.append(_sale)
                return jsonify({"Success":"sale '{0}' added".format(_sale["sale_id"])}), 201

#get all sales
@app.route('/api/v1/sales', methods=['GET'])
def get_sales():
    """get_sales() -- returns all sales"""
    if SALES:
        return jsonify({'sales': SALES})
    else:
        return jsonify({'message': "There are no sale records"})

if __name__ == '__main__':
    app.run(debug=True)
