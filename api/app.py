"""!Flask web api for Store Manager"""
from flask import Flask, jsonify, abort, make_response, request

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

SALES = [
    {
        'product_id': 1,
        'sale_id': 1,
        'product_name': 'Sugar',
        'quantity': '2',
        'date': '2018-10-10',
        'price': '8000',
        'payment': 'cash',
        'attendant': 'johnny'

    },
    {
        'product_id': 1,
        'sale_id': 2,
        'product_name': 'Sugar',
        'quantity': '1',
        'date': '2018-10-12',
        'price': '4000',
        'payment': 'cash',
        'attendant': 'tom'

    },
    {
        'product_id': 6,
        'sale_id': 3,
        'product_name': 'Bic Pens',
        'quantity': '3',
        'date': '2018-10-10',
        'price': '15000',
        'payment': 'cash',
        'attendant': 'johnny'

    }
]
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
        
        prod_name = request.get_json('product_name')
        prod_cat = request.get_json('category')
        prod_price = request.get_json('unit_price')
        prod_qty = request.get_json('quantity')
        prod_meas = request.get_json('measure')

        _product = {
            'product_id':PRODUCTS[-1]['product_id'] + 1,
            'product_name':prod_name,
            'category':prod_cat,
            'unit_price':prod_price,
            'quantity':prod_qty,
            'measure':prod_meas
        }
        PRODUCTS.append(_product)
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
            return "Successfully deleted it", 204
        else:
            abort(404)
    else:
        abort(405)  

#add a sale
@app.route('/api/v1/sales', methods=['POST'])
def create_sale():
    """create_sale() --returns a product that has been added"""
   
    prod_id = request.get_json('product_id')
    prod_name = request.get_json('product_name')
    price_ = request.get_json('price')
    date_ = request.get_json('date')
    prod_qty = request.get_json('quantity')
    payment_ = request.get_json('payment')
    attendant_ = request.get_json('attendant')

    _sale = {
        'sale_id':SALES[-1]['sale_id'] + 1,
        'product_id':prod_id,
        'product_name':prod_name,
        'price':price_,
        'date':date_,
        'quantity':prod_qty,
        'payment':payment_,
        'attendany': attendant_
    }
    SALES.append(_sale)
    return jsonify({"Success":"sale '{0}' added".format(_sale["sale_id"])}), 201


if __name__ == '__main__':
    app.run(debug=True)
