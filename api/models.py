"""structure models"""
class Products:
    """product model"""
    def __init__(self, product_name, category, unit_price, quantity, measure):
        self.product_name = product_name
        self.category = category
        self.unit_price = unit_price
        self.quantity = quantity
        self.measure = measure

class Sales:
    """sale model"""
    def __init__(self, user_id):
        self.user_id = user_id

class SalesHasProducts:
    """sales has products"""
    def __init__(self, sale_id, product_id, quantity, total):
        self.sale_id = sale_id
        self.product_id = product_id
        self.quantity =quantity
        self.total = total
        
class Users:
    """user model"""
    def __init__(self, name, user_name, password, role):
        self.name = name
        self.user_name = user_name
        self.password = password
        self.role = role

class Login:
    """lgin model"""
    def __init__(self, user_name, password, role):
        self.user_name = user_name
        self.password = password
        self.role = role
