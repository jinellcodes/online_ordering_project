from flask import Blueprint, jsonify, abort, request
from ..models import Account, Customer, db
import hashlib
import secrets

bp = Blueprint('accounts', __name__, url_prefix='/accounts')

# function used to "scramble" the password
def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

# Get list of all accounts
@bp.route('', methods=['GET'])
def index():
    print('-- index function --')
    accounts = Account.query.all()
    print('after Account.query.all()')
    result = []
    for a in accounts:
        print('a:', a)
        result.append(a.serialize())
    return jsonify(result)

# Get details for a single account

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    a = Account.query.get_or_404(id)
    return jsonify(a.serialize())

# POST - create a new account
@bp.route('', methods=['POST'])
def create():
    # JSON request body must have username, password, email
    if 'username' not in request.json or 'password' not in request.json or 'email' not in request.json:
        return abort(400)
    # Create account
    # use scramble function on password being passed to Account class
    a = Account(
        username=request.json['username'],
        password=scramble(request.json['password']),
        email=request.json['email'],
        phone=request.json['phone']
    )
    db.session.add(a)
    db.session.commit()
    return jsonify(a.serialize())

# DELETE - delete account
@bp.route('/<int:id>', methods=['DELETE'])
def delete(id:int):
    a = Account.query.get_or_404(id)
    try:
        db.session.delete(a)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)