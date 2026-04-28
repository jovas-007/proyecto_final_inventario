from flask import Blueprint, send_file, jsonify
from pdf_generator import (
    generar_inventario_completo,
    generar_stock_bajo,
    generar_reporte_categorias,
    generar_reporte_proveedores,
)

reportes_bp = Blueprint('reportes', __name__, url_prefix='/reportes')


@reportes_bp.route('/inventario', methods=['GET'])
def reporte_inventario():
    """Genera PDF del inventario completo."""
    try:
        pdf_buffer = generar_inventario_completo()
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='inventario_completo.pdf',
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reportes_bp.route('/stock-bajo', methods=['GET'])
def reporte_stock_bajo():
    """Genera PDF de productos con stock bajo."""
    try:
        pdf_buffer = generar_stock_bajo()
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='stock_bajo.pdf',
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reportes_bp.route('/categorias', methods=['GET'])
def reporte_categorias():
    """Genera PDF del reporte por categorías."""
    try:
        pdf_buffer = generar_reporte_categorias()
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='reporte_categorias.pdf',
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reportes_bp.route('/proveedores', methods=['GET'])
def reporte_proveedores():
    """Genera PDF del reporte de proveedores."""
    try:
        pdf_buffer = generar_reporte_proveedores()
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='reporte_proveedores.pdf',
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
