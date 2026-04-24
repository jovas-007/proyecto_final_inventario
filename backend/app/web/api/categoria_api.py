from flask import Blueprint, request, jsonify
from app.core.use_cases.categoria_use_cases import CategoriaUseCases
from app.data.repositories.categoria_repository import CategoriaRepository

categoria_bp = Blueprint('categorias', __name__, url_prefix='/api/categorias')
use_cases = CategoriaUseCases(CategoriaRepository())


@categoria_bp.route('/', methods=['GET'])
def listar():
    categorias = use_cases.listar_categorias()
    return jsonify({'success': True, 'data': [c.to_dict() for c in categorias]})


@categoria_bp.route('/<int:categoria_id>', methods=['GET'])
def obtener(categoria_id):
    categoria = use_cases.obtener_categoria(categoria_id)
    if not categoria:
        return jsonify({'success': False, 'error': 'Categoría no encontrada'}), 404
    return jsonify({'success': True, 'data': categoria.to_dict()})


@categoria_bp.route('/', methods=['POST'])
def crear():
    try:
        data = request.get_json()
        categoria = use_cases.crear_categoria(data)
        return jsonify({'success': True, 'data': categoria.to_dict()}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@categoria_bp.route('/<int:categoria_id>', methods=['PUT'])
def actualizar(categoria_id):
    try:
        data = request.get_json()
        categoria = use_cases.actualizar_categoria(categoria_id, data)
        return jsonify({'success': True, 'data': categoria.to_dict()})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@categoria_bp.route('/<int:categoria_id>', methods=['DELETE'])
def eliminar(categoria_id):
    eliminado = use_cases.eliminar_categoria(categoria_id)
    if not eliminado:
        return jsonify({'success': False, 'error': 'Categoría no encontrada'}), 404
    return jsonify({'success': True, 'data': 'Categoría eliminada'})


@categoria_bp.route('/stats', methods=['GET'])
def stats():
    return jsonify({
        'success': True,
        'data': {
            'total_categorias': use_cases.contar_categorias(),
        }
    })
