import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')

    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '4000')
    DB_USERNAME = os.getenv('DB_USERNAME', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_DATABASE = os.getenv('DB_DATABASE', 'inventario_proyecto')

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
        f"?ssl_verify_cert=false&ssl_verify_identity=false"
    )

    # Redis para microservicio de notificaciones
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True,
        'connect_args': {
            'ssl': {
                'ssl_mode': 'VERIFY_IDENTITY',
                'check_hostname': False,
            }
        }
    }
