"""!Flask web api for Store Manager"""
from flask import Flask, jsonify, abort, make_response, request

NOT_FOUND = 'Not found'
BAD_REQUEST = 'Bad request'

app = Flask(__name__)
"""initializing"""

PRODUCTS = [
    {
        'product_id': 1,
        'product_name': 'Sugar',
        'category': 'Food',
        'unit_price': 4000,
        'quantity' : '100',
        'measure' : 'Kg'
    },
    {
        'product_id': 2,
        'product_name': 'Ariel-Small',
        'category': 'Detergent',
        'unit_price': 500,
        'quantity' : '40',
        'measure' : 'Pkts'
    },
    {
        'product_id': 3,
        'product_name': 'Ariel-Big',
        'category': 'Detergent',
        'unit_price': 2000,
        'quantity' : '35',
        'measure': 'Pkts'
    },
    {
        'product_id': 4,
        'product_name': 'Broom',
        'category': 'Home Utilities',
        'unit_price': 1000,
        'quantity' : '10',
        'measure': 'Sticks'
    },
    {
        'product_id': 5,
        'product_name': '98-Paged Picfare Books',
        'category': 'Scholastic Materials',
        'unit_price': 4800,
        'quantity' : '144',
        'measure': 'Dozens'
    },
    {
        'product_id': 6,
        'product_name': 'Bic Pens',
        'category': 'Scholastic Materials',
        'unit_price': 5000,
        'quantity' : '12',
        'measure': 'Box'
    },
    {
        'product_id': 6,
        'product_name': 'Vanilla Sponge Cake',
        'category': 'Baked Goodies',
        'unit_price': 7500,
        'quantity' : '3',
        'measure': 'Slices'
    },
    {
        'product_id': 7,
        'product_name': 'Always',
        'category': 'Women Products',
        'unit_price': 3000,
        'quantity' : '12',
        'measure': 'Pkts'
    },
    {
        'product_id': 8,
        'product_name': 'Vaseline Cocoa',
        'category': 'Women Products',
        'unit_price': 12000,
        'quantity' : '10',
        'measure': 'Bottles'
    },
    {
        'product_id': 9,
        'product_name': 'Vaseline Cocoa',
        'category': 'Men Products',
        'unit_price': 12000,
        'quantity' : '10',
        'measure': 'Bottles'
    },
    {
        'product_id': 10,
        'product_name': 'Vaseline Men',
        'category': 'Men Products',
        'unit_price': 10000,
        'quantity' : '10',
        'measure': 'Bottles'
    },
    {
        'product_id': 11,
        'product_name': 'Zesta Strawberry Jam',
        'category': 'Food',
        'unit_price': 7500,
        'quantity' : '5',
        'measure': 'Bottles'
    }
]

#error handlers
@app.errorhandler(404)
def not_found(error):
    """ not_found(error) -returns error not found"""
    return make_response(jsonify({'error': NOT_FOUND}), 404)

@app.errorhandler(400)
def bad_request(error):
    """ bad_request(error) -returns error bad request"""
    return make_response(jsonify({'error': BAD_REQUEST}), 400)

@app.errorhandler(500)
def bad_request(error):
    """ bad_request(error) -returns error bad request"""
    return make_response(jsonify({'error': "Server error"}), 500)

#home
@app.route('/storemanager/api/v1.0/')
def home():
    """home()--this is home"""
    return jsonify({"Welcome": "Welcome to the Store Manger API"})
def _get_product(productid):
    """_get_product(productid) returns a product in products via product_id"""
    return [product for product in PRODUCTS if product['product_id'] == productid]

#get all products
@app.route('/storemanager/api/v1.0/products', methods=['GET'])
def get_products():
    """get_products() -- returns all products"""
    return jsonify({'products': PRODUCTS})
    
#get specific product
@app.route('/storemanager/api/v1.0/products/<int:_id>', methods=['GET'])
def get_product(_id):
    """get_product(_id) -- returns a product via its id"""
    _product_ = _get_product(_id)
    if not _product_:
        abort(404)
    return jsonify({'products': _product_})

if __name__ == '__main__':
    app.run(debug=True)
