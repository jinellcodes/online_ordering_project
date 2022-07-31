from flask import Blueprint, jsonify, abort, request
from ..models import Product, db

bp = Blueprint('products', __name__, url_prefix='/products')

# GET - index of all products in database and their info
@bp.route('', methods=['GET'])
def index():
    products = Product.query.all()
    result = []
    for p in products:
        result.append(p.serialize())
    return jsonify(result)

# GET - details about a specific product using ID
@bp.route('/<int:id>', methods=['GET'])
def show(id:int):
    p = Product.query.get_or_404(id)
    return jsonify(p.serialize())

# POST - create new product

@bp.route('', methods=['POST'])
def create():
    # request body must contain the values that are non-nullable
    if 'name' not in request.json or 'price' not in request.json or 'weight' not in request.json or 'quantity' not in request.json:
        return abort(400)
    p = Product(
        name=request.json['name'],
        price=request.json['price'],
        weight=request.json['weight'],
        quantity=request.json['quantity']
    )
    db.session.add(p)
    db.session.commit()
    return jsonify(p.serialize())

# DELETE - delete product
@bp.route('/<int:id>', methods=['DELETE'])
def delete(id:int):
    p = Product.query.get_or_404(id)
    try:
        db.session.delete(p)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)