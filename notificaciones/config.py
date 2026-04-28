import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
RESEND_API_KEY = os.getenv('RESEND_API_KEY', '')
ALERT_EMAIL_TO = os.getenv('ALERT_EMAIL_TO', 'jovassolis2@gmail.com')
ALERT_EMAIL_FROM = os.getenv('ALERT_EMAIL_FROM', 'StockPro Alertas <inventario@icybarber.me>')
