"""
WSGI entrypoint for production servers (e.g., Render + Gunicorn).
"""

from app import create_app
from config import get_config

app = create_app(get_config())
