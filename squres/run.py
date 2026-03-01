"""
SQURES Flask Application Runner
"""

import os
import sys
from app import create_app

if __name__ == '__main__':
    # Create Flask app
    app = create_app()
    
    # Run development server
    app.run(
        debug=True,
        host='0.0.0.0',
        port=8000,
        use_reloader=True
    )
