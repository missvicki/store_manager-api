"""database models"""
class Products:
    """product model"""
    def __init__(self, product_name, category, unit_price, quantity, measure, date):
        self.product_name = product_name
        self.category = category
        self.unit_price = unit_price
        self.quantity = quantity
        self.measure = measure
        self.date = date

class Sales:
    """sale model"""
    def __init__(self, product_id, user_id, quantity, total, date):
        self.product_id = product_id
        self.user_id = user_id
        self.quantity = quantity
        self.total = total
        self.date = date

class Users:
    """user model"""
    def __init__(self, name, user_name, password, role, date):
        # self.user_id = user_id
        self.name = name
        self.user_name = user_name
        self.password = password
        self.role = role
        self.date = date
