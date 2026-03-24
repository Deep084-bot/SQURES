"""
Configuration for SQURES application.
Supports different environments (development, testing, production).
"""

import os


class Config:
    """Base configuration."""
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500 MB
    UPLOAD_FOLDER = '/tmp/squres_uploads'
    
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    UPLOAD_FOLDER = '/tmp/squres_test'


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False

    def __init__(self):
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY environment variable must be set in production")


def get_config(env=None):
    """Get configuration based on environment."""
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')
    
    config_map = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig
    }
    
    return config_map.get(env, DevelopmentConfig)
