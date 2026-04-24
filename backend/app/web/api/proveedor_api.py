from flask import Blueprint, request, jsonify
from app.core.use_cases.proveedor_use_cases import ProveedorUseCases
from app.data.repositories.proveedor_repository import ProveedorRepository

proveedor_bp = Blueprint('proveedores', __name__, url_prefix='/api/proveedores')
use_cases = ProveedorUseCases(ProveedorRepository())


@proveedor_bp.route('/', methods=['GET'])
def listar():
    proveedores = use_cases.listar_proveedores()
    return jsonify({'success': True, 'data': [p.to_dict() for p in proveedores]})


@proveedor_bp.route('/<int:proveedor_id>', methods=['GET'])
def obtener(proveedor_id):
    proveedor = use_cases.obtener_proveedor(proveedor_id)
    if not proveedor:
        return jsonify({'success': False, 'error': 'Proveedor no encontrado'}), 404
    return jsonify({'success': True, 'data': proveedor.to_dict()})


@proveedor_bp.route('/', methods=['POST'])
def crear():
    try:
        data = request.get_json()
        proveedor = use_cases.crear_proveedor(data)
        return jsonify({'success': True, 'data': proveedor.to_dict()}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@proveedor_bp.route('/<int:proveedor_id>', methods=['PUT'])
def actualizar(proveedor_id):
    try:
        data = request.get_json()
        proveedor = use_cases.actualizar_proveedor(proveedor_id, data)
        return jsonify({'success': True, 'data': proveedor.to_dict()})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@proveedor_bp.route('/<int:proveedor_id>', methods=['DELETE'])
def eliminar(proveedor_id):
    eliminado = use_cases.eliminar_proveedor(proveedor_id)
    if not eliminado:
        return jsonify({'success': False, 'error': 'Proveedor no encontrado'}), 404
    return jsonify({'success': True, 'data': 'Proveedor eliminado'})


@proveedor_bp.route('/stats', methods=['GET'])
def stats():
    return jsonify({
        'success': True,
        'data': {
            'total_proveedores': use_cases.contar_proveedores(),
        }
    })
