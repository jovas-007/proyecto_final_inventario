import json
import logging
import redis
from config.config import Config

logger = logging.getLogger(__name__)


class EventPublisher:
    """Publica eventos en Redis para que los microservicios los consuman."""

    _client = None

    @classmethod
    def _get_client(cls):
        if cls._client is None:
            try:
                cls._client = redis.from_url(
                    Config.REDIS_URL,
                    decode_responses=True,
                    socket_connect_timeout=3,
                )
                cls._client.ping()
                logger.info("✓ Conectado a Redis para eventos")
            except Exception as e:
                logger.warning(f"⚠ Redis no disponible: {e}")
                cls._client = None
        return cls._client

    @classmethod
    def publicar_alerta_stock(cls, producto_data: dict):
        """
        Publica una alerta de stock bajo en el canal 'stock_alerts'.
        Si Redis no está disponible, falla silenciosamente sin
        afectar el flujo principal del CRUD.
        """
        try:
            client = cls._get_client()
            if client is None:
                return False

            evento = {
                'tipo': 'stock_bajo',
                'producto': {
                    'id': producto_data.get('id'),
                    'nombre': producto_data.get('nombre'),
                    'codigo_barras': producto_data.get('codigo_barras', ''),
                    'stock_actual': producto_data.get('stock_actual'),
                    'stock_minimo': producto_data.get('stock_minimo'),
                    'precio_venta': producto_data.get('precio_venta'),
                    'proveedor_nombre': producto_data.get('proveedor_nombre', 'Sin proveedor'),
                    'categoria_nombre': producto_data.get('categoria_nombre', 'Sin categoría'),
                },
            }

            client.publish('stock_alerts', json.dumps(evento))
            logger.info(
                f"📢 Alerta publicada: {producto_data.get('nombre')} "
                f"(stock: {producto_data.get('stock_actual')}/{producto_data.get('stock_minimo')})"
            )
            return True

        except Exception as e:
            logger.error(f"Error publicando evento: {e}")
            # Resetear conexión para reconectar en el próximo intento
            cls._client = None
            return False
