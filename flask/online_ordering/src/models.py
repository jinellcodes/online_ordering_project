import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(319), nullable=False)
    shipping_address = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=True)

    def __init__(self, first_name: str, last_name: str, email: str, shipping_address: str, phone: str, account_id: int):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.shipping_address = shipping_address
        self.phone = phone
        self.account_id = account_id

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'shipping_address': self.shipping_address,
            'phone': self.phone,
            'account_id': self.account_id
        }
    
class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(319), unique=True, nullable=False)
    phone = db.Column(db.String(15))
    # research these parts; lazy? uselist?
    # foreign key isn't working... why??
    # customer = db.relationship('Account', backref='customers', lazy=True, uselist=False)

    def __init__(self, username: str, password: str, email: str, phone: str):
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
    
    def serialize(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone
        }

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)

    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name
    
    def serialize(self):
        return{
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name
        }

# Bridge table - create orders_products table to implement many-to-many relationship
# Use the db.Table() function to create a table with 2 columns; best practice to use a table instead of a database model.
# orders_products table has 2 columns representing 2 foreign keys
# Below this table are the 2 models representing the tables 'orders' and 'products'

orders_products = db.Table('orders_products', 
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
    )

# Many-to-many relationship
# Add a products class variable to the Order model (ie products = [...])
# Use the db.relationship() method, passing it the name of the products model 
# Pas the orders_products association table (bridge table) to the secondary parameter to establish a many-to-many relationship between orders and products
# Use the backref parameter to add a back reference that behaves like a column to the orders model; that way you can access the order's products via order.products and products of orders via product.orders

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    total_weight = db.Column(db.Float, nullable=False)
    shipping_cost = db.Column(db.Float, nullable=False)
    products_cost = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    products = db.relationship('Product', secondary=orders_products, backref='orders')

    def __init__(self, total_weight: float, shipping_cost: float, products_cost: float, total_amount: float, customer_id: int, employee_id: int):
        self.total_weight = total_weight
        self.shipping_cost = shipping_cost
        self.products_cost = products_cost
        self.total_amount = total_amount
        self.customer_id = customer_id
        self.employee_id = employee_id

    def serialize(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'total_weight': self.total_weight,
            'shipping_cost': self.shipping_cost,
            'products_cost': self.products_cost,
            'total_amount': self.total_amount,
            'customer_id': self.customer_id,
            'employee_id': self.employee_id
        }

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, name: str, price: float, weight: float, quantity: int):
        self.name = name
        self.price = price
        self.weight = weight
        self.quantity = quantity
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'weight': self.weight,
            'quantity': self.quantity
        }


