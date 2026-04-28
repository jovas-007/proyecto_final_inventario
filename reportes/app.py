"""
Microservicio de Reportes PDF
==============================
API Flask independiente que genera reportes PDF del inventario.
Se conecta directamente a TiDB para leer datos.

Tipos de reportes:
- Inventario completo
- Productos con stock bajo
- Reporte por categorías
- Reporte de proveedores
"""

import os
from flask import Flask, send_file, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, resources={r"/reportes/*": {"origins": "*"}})
    db.init_app(app)

    from routes import reportes_bp
    app.register_blueprint(reportes_bp)

    @app.route('/')
    def index():
        return jsonify({
            'message': 'Microservicio de Reportes PDF',
            'version': '1.0.0',
            'endpoints': [
                '/reportes/inventario',
                '/reportes/stock-bajo',
                '/reportes/categorias',
                '/reportes/proveedores',
            ]
        })

    return app


app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8081))
    app.run(host='0.0.0.0', port=port, debug=True)
