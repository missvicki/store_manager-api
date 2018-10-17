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
#get all products
@app.route('storemanager/api/v1.0/products', methods=['GET'])
def get_products():
    """get_products() -- returns all products"""
    return jsonify({'products': PRODUCTS})

if __name__ == '__main__':
    app.run(debug=True)
