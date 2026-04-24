import os
import sys

# Agregar backend/ al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_cors import CORS
from config.config import Config
from app.data.database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Habilitar CORS para desarrollo en localhost
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Inicializar base de datos
    db.init_app(app)

    # Registrar blueprints
    from app.web.api.producto_api import producto_bp
    from app.web.api.categoria_api import categoria_bp
    from app.web.api.proveedor_api import proveedor_bp

    app.register_blueprint(producto_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(proveedor_bp)

    # Crear tablas si no existen
    with app.app_context():
        # Importar modelos para que SQLAlchemy los registre
        from app.data.models.categoria_model import CategoriaModel
        from app.data.models.proveedor_model import ProveedorModel
        from app.data.models.producto_model import ProductoModel
        db.create_all()
        print("✓ Base de datos conectada y tablas creadas")

    @app.route('/')
    def index():
        return {'message': 'API Sistema de Inventario', 'version': '1.0.0'}

    return app


app = create_app()

if __name__ == '__main__':
    print("=" * 50)
    print("  Sistema de Inventario - API REST")
    print("  http://127.0.0.1:8080")
    print("=" * 50)
    app.run(host='0.0.0.0', port=8080, debug=True)
