"""
SQARES - Software Quality Analysis and Realiability Evaluation System
Flask application factory
"""

from flask import Flask


def create_app(config=None):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB max upload size
    app.config['UPLOAD_FOLDER'] = '/tmp/squres_uploads'
    
    if config:
        if isinstance(config, dict):
            app.config.update(config)
        else:
            app.config.from_object(config)
    
    from app.routes import api_bp, web_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(web_bp)
    
    return app
