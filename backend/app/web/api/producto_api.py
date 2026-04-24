from flask import Blueprint, request, jsonify
from app.core.use_cases.producto_use_cases import ProductoUseCases
from app.data.repositories.producto_repository import ProductoRepository

producto_bp = Blueprint('productos', __name__, url_prefix='/api/productos')
use_cases = ProductoUseCases(ProductoRepository())


@producto_bp.route('/', methods=['GET'])
def listar():
    productos = use_cases.listar_productos()
    return jsonify({'success': True, 'data': [p.to_dict() for p in productos]})


@producto_bp.route('/<int:producto_id>', methods=['GET'])
def obtener(producto_id):
    producto = use_cases.obtener_producto(producto_id)
    if not producto:
        return jsonify({'success': False, 'error': 'Producto no encontrado'}), 404
    return jsonify({'success': True, 'data': producto.to_dict()})


@producto_bp.route('/', methods=['POST'])
def crear():
    try:
        data = request.get_json()
        producto = use_cases.crear_producto(data)
        return jsonify({'success': True, 'data': producto.to_dict()}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@producto_bp.route('/<int:producto_id>', methods=['PUT'])
def actualizar(producto_id):
    try:
        data = request.get_json()
        producto = use_cases.actualizar_producto(producto_id, data)
        return jsonify({'success': True, 'data': producto.to_dict()})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@producto_bp.route('/<int:producto_id>', methods=['DELETE'])
def eliminar(producto_id):
    eliminado = use_cases.eliminar_producto(producto_id)
    if not eliminado:
        return jsonify({'success': False, 'error': 'Producto no encontrado'}), 404
    return jsonify({'success': True, 'data': 'Producto eliminado'})


@producto_bp.route('/bajo-stock', methods=['GET'])
def bajo_stock():
    productos = use_cases.obtener_bajo_stock()
    return jsonify({'success': True, 'data': [p.to_dict() for p in productos]})


@producto_bp.route('/stats', methods=['GET'])
def stats():
    return jsonify({
        'success': True,
        'data': {
            'total_productos': use_cases.contar_productos(),
            'bajo_stock': use_cases.contar_bajo_stock(),
            'valor_inventario': use_cases.valor_total_inventario(),
        }
    })
