import logging
from flask import Blueprint, send_file, jsonify
from pdf_generator import (
    generar_inventario_completo,
    generar_stock_bajo,
    generar_reporte_categorias,
    generar_reporte_proveedores,
)

logger = logging.getLogger(__name__)
reportes_bp = Blueprint('reportes', __name__, url_prefix='/reportes')


@reportes_bp.route('/inventario', methods=['GET'])
def reporte_inventario():
    logger.info("📄 Solicitud de reporte: Inventario Completo")
    try:
        logger.info("⏳ Consultando base de datos...")
        pdf_buffer = generar_inventario_completo()
        size = pdf_buffer.getbuffer().nbytes
        logger.info(f"✅ PDF generado exitosamente — tamaño: {size} bytes")
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='inventario_completo.pdf',
        )
    except Exception as e:
        logger.error(f"❌ Error generando inventario: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


@reportes_bp.route('/stock-bajo', methods=['GET'])
def reporte_stock_bajo():
    logger.info("📄 Solicitud de reporte: Stock Bajo")
    try:
        pdf_buffer = generar_stock_bajo()
        size = pdf_buffer.getbuffer().nbytes
        logger.info(f"✅ PDF stock-bajo generado — tamaño: {size} bytes")
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='stock_bajo.pdf',
        )
    except Exception as e:
        logger.error(f"❌ Error generando stock-bajo: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


@reportes_bp.route('/categorias', methods=['GET'])
def reporte_categorias():
    logger.info("📄 Solicitud de reporte: Categorías")
    try:
        pdf_buffer = generar_reporte_categorias()
        size = pdf_buffer.getbuffer().nbytes
        logger.info(f"✅ PDF categorías generado — tamaño: {size} bytes")
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='reporte_categorias.pdf',
        )
    except Exception as e:
        logger.error(f"❌ Error generando categorías: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


@reportes_bp.route('/proveedores', methods=['GET'])
def reporte_proveedores():
    logger.info("📄 Solicitud de reporte: Proveedores")
    try:
        pdf_buffer = generar_reporte_proveedores()
        size = pdf_buffer.getbuffer().nbytes
        logger.info(f"✅ PDF proveedores generado — tamaño: {size} bytes")
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='reporte_proveedores.pdf',
        )
    except Exception as e:
        logger.error(f"❌ Error generando proveedores: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


@reportes_bp.route('/health', methods=['GET'])
def health():
    """Endpoint de diagnóstico para verificar que el servicio responde."""
    from models import ProductoModel, CategoriaModel, ProveedorModel
    try:
        n_productos = ProductoModel.query.filter_by(activo=True).count()
        n_categorias = CategoriaModel.query.count()
        n_proveedores = ProveedorModel.query.count()
        logger.info(f"🩺 Health check OK — productos={n_productos}, categorias={n_categorias}, proveedores={n_proveedores}")
        return jsonify({
            'status': 'ok',
            'productos': n_productos,
            'categorias': n_categorias,
            'proveedores': n_proveedores,
        })
    except Exception as e:
        logger.error(f"❌ Health check falló: {e}", exc_info=True)
        return jsonify({'status': 'error', 'error': str(e)}), 500
