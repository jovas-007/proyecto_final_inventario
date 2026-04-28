from flask import Blueprint, jsonify
from app.core.use_cases.producto_use_cases import ProductoUseCases
from app.data.repositories.producto_repository import ProductoRepository

notificacion_bp = Blueprint('notificaciones', __name__, url_prefix='/api/notificaciones')
producto_uc = ProductoUseCases(ProductoRepository())


@notificacion_bp.route('/alertas-activas', methods=['GET'])
def alertas_activas():
    """Devuelve los productos que actualmente están por debajo del stock mínimo."""
    try:
        productos_bajo_stock = producto_uc.obtener_bajo_stock()
        alertas = []
        for p in productos_bajo_stock:
            d = p.to_dict()
            # Clasificar severidad
            if p.stock_actual == 0:
                severidad = 'agotado'
            elif p.stock_actual <= (p.stock_minimo // 2):
                severidad = 'critico'
            else:
                severidad = 'bajo'
            d['severidad'] = severidad
            alertas.append(d)

        return jsonify({
            'success': True,
            'data': alertas,
            'resumen': {
                'total_alertas': len(alertas),
                'agotados': sum(1 for a in alertas if a['severidad'] == 'agotado'),
                'criticos': sum(1 for a in alertas if a['severidad'] == 'critico'),
                'bajos': sum(1 for a in alertas if a['severidad'] == 'bajo'),
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
