from flask import Blueprint, request, jsonify
from .. import db
from ..models import Material

main = Blueprint('main', __name__)

@main.route('/materials', methods=['POST'])
def add_material():
    
    data = request.get_json()
    if not data or not data.get('name') or data.get('quantuty') is None:
        return jsonify({'error': 'Faltan campos'}), 400
    try:
        material = Material(
            name=data['name'],
            description=data.get('description', ''),
            quantuty=data['quantuty']
        )
        db.session.add(material)
        db.session.commit()
        return jsonify({'message': 'Material creado', 'id': material.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/materials', methods=['GET'])
def get_materials():

    materials = Material.query.all()
    result = []
    for m in materials:
      result.append({
        'id': m.id,
        'name': m.name,
        'description': m.description,
        'quantuty': m.quantuty
            })
    return jsonify(result)
