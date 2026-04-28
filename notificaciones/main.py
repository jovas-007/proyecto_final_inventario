"""
Microservicio de Notificaciones — Stock Bajo
=============================================
Escucha eventos de Redis (canal: stock_alerts) y envía correos
electrónicos de alerta cuando un producto alcanza su stock mínimo.

Arquitectura: Worker (no expone puerto HTTP)
Comunicación: Redis Pub/Sub
Email: Resend API
"""

import json
import time
import logging
import sys

import redis
from config import REDIS_URL
from email_service import enviar_alerta

# ── Configurar logging ──
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger('notificaciones')


def procesar_mensaje(mensaje: dict):
    """Procesa un mensaje recibido del canal de Redis."""
    try:
        data = json.loads(mensaje['data'])
        tipo = data.get('tipo')

        if tipo == 'stock_bajo':
            producto = data.get('producto', {})
            logger.info(
                f"📦 Alerta recibida: {producto.get('nombre')} "
                f"(stock: {producto.get('stock_actual')}/{producto.get('stock_minimo')})"
            )
            enviado = enviar_alerta(producto)
            if enviado:
                logger.info("✉️  Correo enviado exitosamente")
            else:
                logger.warning("⚠️  No se pudo enviar el correo")
        else:
            logger.warning(f"Tipo de evento desconocido: {tipo}")

    except json.JSONDecodeError as e:
        logger.error(f"Error decodificando JSON: {e}")
    except Exception as e:
        logger.error(f"Error procesando mensaje: {e}")


def main():
    """Bucle principal: se conecta a Redis y escucha eventos."""
    logger.info("=" * 50)
    logger.info("  Microservicio de Notificaciones")
    logger.info("  Escuchando canal: stock_alerts")
    logger.info("=" * 50)

    while True:
        try:
            client = redis.from_url(
                REDIS_URL,
                decode_responses=True,
                socket_connect_timeout=5,
            )
            client.ping()
            logger.info("✓ Conectado a Redis")

            pubsub = client.pubsub()
            pubsub.subscribe('stock_alerts')
            logger.info("✓ Suscrito al canal 'stock_alerts'")

            for mensaje in pubsub.listen():
                if mensaje['type'] == 'message':
                    procesar_mensaje(mensaje)

        except redis.ConnectionError as e:
            logger.error(f"✗ Conexión a Redis perdida: {e}")
            logger.info("Reintentando en 5 segundos...")
            time.sleep(5)

        except KeyboardInterrupt:
            logger.info("Apagando microservicio...")
            break

        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            logger.info("Reintentando en 10 segundos...")
            time.sleep(10)


if __name__ == '__main__':
    main()
