"""
SQURES Flask Application Runner
"""

import os
import sys
from app import create_app
from config import get_config

if __name__ == '__main__':
    # Create Flask app
    app = create_app(get_config())
    
    # Run development server
    app.run(
        debug=app.config.get('DEBUG', True),
        host='0.0.0.0',
        port=8000,
        use_reloader=True
    )
