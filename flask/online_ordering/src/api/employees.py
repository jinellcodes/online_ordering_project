from flask import Blueprint, jsonify, abort, request
from ..models import Employee, Order, db

bp = Blueprint('employees', __name__, url_prefix='/employees')

# GET - show list of employees
@bp.route('', methods=['GET'])
def index():
    employees = Employee.query.all()
    result = []
    for e in employees:
        result.append(e.serialize())
    return jsonify(result)

# GET - show specific employee data using ID
@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    e = Employee.query.get_or_404(id)
    return jsonify(e.serialize())

# POST - create new employee
@bp.route('', methods=['POST'])
def create():
    # request body must contain the values that are non-nullable
    if 'first_name' not in request.json or 'last_name' not in request.json:
        return abort(400)
    e = Employee(
        first_name=request.json['first_name'],
        last_name=request.json['last_name']
    )
    db.session.add(e)
    db.session.commit()
    return jsonify(e.serialize())

# DELETE - delete employee
@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    e = Employee.query.get_or_404(id)
    try:
        db.session.delete(e)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)