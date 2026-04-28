import logging
import resend
from config import RESEND_API_KEY, ALERT_EMAIL_TO, ALERT_EMAIL_FROM

logger = logging.getLogger(__name__)

# Configurar API Key de Resend
resend.api_key = RESEND_API_KEY


def _cargar_template(producto: dict) -> str:
    """Genera el HTML del correo de alerta con los datos del producto."""
    nombre = producto.get('nombre', 'Producto desconocido')
    stock_actual = producto.get('stock_actual', 0)
    stock_minimo = producto.get('stock_minimo', 5)
    proveedor = producto.get('proveedor_nombre', 'Sin proveedor')
    categoria = producto.get('categoria_nombre', 'Sin categoría')
    codigo = producto.get('codigo_barras', '—')
    precio = producto.get('precio_venta', 0)

    # Color de severidad
    if stock_actual == 0:
        color_badge = '#ef4444'
        texto_nivel = 'AGOTADO'
    elif stock_actual <= (stock_minimo // 2):
        color_badge = '#f97316'
        texto_nivel = 'CRITICO'
    else:
        color_badge = '#eab308'
        texto_nivel = 'BAJO'

    try:
        with open('templates/alerta_stock.html', 'r', encoding='utf-8') as f:
            template = f.read()
        return template.format(
            nombre=nombre,
            stock_actual=stock_actual,
            stock_minimo=stock_minimo,
            proveedor=proveedor,
            categoria=categoria,
            codigo=codigo,
            precio=f"${precio:.2f}",
            color_badge=color_badge,
            texto_nivel=texto_nivel,
        )
    except FileNotFoundError:
        return f"""
        <h2>Alerta de Stock Bajo</h2>
        <p><b>{nombre}</b> tiene stock bajo.</p>
        <p>Stock actual: {stock_actual} | Stock minimo: {stock_minimo}</p>
        <p>Proveedor: {proveedor}</p>
        """


def enviar_alerta(producto: dict) -> bool:
    """Envía un correo de alerta de stock bajo usando Resend."""
    if not RESEND_API_KEY:
        logger.warning("[WARN] RESEND_API_KEY no configurada, no se envia correo")
        return False

    nombre = producto.get('nombre', 'Producto')
    stock_actual = producto.get('stock_actual', 0)

    try:
        html_content = _cargar_template(producto)

        params = {
            "from": ALERT_EMAIL_FROM,
            "to": [ALERT_EMAIL_TO],
            "subject": f"[STOCK BAJO] {nombre} ({stock_actual} unidades)",
            "html": html_content,
        }

        email = resend.Emails.send(params)
        logger.info(f"[OK] Correo enviado para '{nombre}' -> {ALERT_EMAIL_TO} (ID: {email.get('id', 'N/A')})")
        return True

    except Exception as e:
        logger.error(f"[ERROR] Enviando correo: {e}")
        return False
