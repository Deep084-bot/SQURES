"""
SQURES Flask Application Runner
"""

from app import create_app
from config import get_config

if __name__ == '__main__':
    app = create_app(get_config())
    
    app.run(
        debug=app.config.get('DEBUG', True),
        host='0.0.0.0',
        port=8000,
        use_reloader=True
    )
