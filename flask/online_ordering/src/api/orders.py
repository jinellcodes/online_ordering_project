from flask import Blueprint, jsonify, abort, request
from ..models import Order, Product, Employee, Customer, db

bp = Blueprint('orders', __name__, url_prefix='/orders')

# GET - index of orders
@bp.route('', methods=['GET'])
def index():
    orders = Order.query.all()
    result = []
    for o in orders:
        result.append(o.serialize())
    return jsonify(result)

# GET - details about a specific order using ID
@bp.route('/<int:id>', methods=['GET'])
def show(id:int):
    o = Order.query.get_or_404(id)
    return jsonify(o.serialize())

# POST - create new order
@bp.route('', methods=['POST'])
def create():
    # request body must contain the values that are non-nullable
    if 'total_weight' not in request.json or 'shipping_cost' not in request.json or 'products_cost' not in request.json or 'total_amount' not in request.json or 'customer_id' not in request.json or 'employee_id' not in request.json:
        return abort(400)
    o = Order(
        total_weight=request.json['total_weight'],
        shipping_cost=request.json['shipping_cost'],
        products_cost=request.json['products_cost'],
        total_amount=request.json['total_amount'],
        customer_id=request.json['customer_id'],
        employee_id=request.json['employee_id']
    )
    db.session.add(o)
    db.session.commit()
    return jsonify(o.serialize())

# DELETE - delete order using ID
@bp.route('/<int:id>', methods=['DELETE'])
def delete(id:int):
    o = Order.query.get_or_404(id)
    try:
        db.session.delete(o)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)