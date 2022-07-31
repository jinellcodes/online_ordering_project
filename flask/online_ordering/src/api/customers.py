from flask import Blueprint, jsonify, abort, request
from ..models import Customer, Account, Order, db

bp = Blueprint('customers', __name__, url_prefix='/customers')

# GET list of customers and all their information
@bp.route('', methods=['GET'])
def index():
    print('-- index function --')
    customers = Customer.query.all()
    print('after Customer.query.all()')
    result = []
    for c in customers:
        print('c:', c)
        result.append(c.serialize())
    return jsonify(result)
    # customers = Customer.query.all()
    # result = []
    # for c in customers:
    #     result.append(c.serialize())
    # return jsonify(result)

# GET details for a single customer using ID number
@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    c = Customer.query.get_or_404(id)
    return jsonify(c.serialize())

# POST - creating a new customer 
@bp.route('', methods=['POST'])
def create():
    # request body must contain the values that are non-nullable
    if 'first_name' not in request.json or 'last_name' not in request.json or 'email' not in request.json or 'shipping_address' not in request.json:
        return abort(400)
    c = Customer(
        first_name=request.json['first_name'],
        last_name=request.json['last_name'],
        email=request.json['email'],
        shipping_address=request.json['shipping_address'],
        phone=request.json['phone'],
        account_id=request.json['account_id']
    )
    db.session.add(c)
    db.session.commit()
    return jsonify(c.serialize())

# DELETE - delete a customer 
@bp.route('/<int:id>', methods=['DELETE'])
def delete(id:int):
    c = Customer.query.get_or_404(id)
    try:
        db.session.delete(c)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)