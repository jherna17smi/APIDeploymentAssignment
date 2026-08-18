import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    API_KEY = os.getenv("API_KEY", "teacher-demo-key")
    APP_HOST = os.getenv("APP_HOST", "127.0.0.1:5000")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")
    DEBUG = False
    TESTING = False
    SWAGGER_SCHEMES = ["http"]


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    APP_HOST = os.getenv("APP_HOST", "your-app.onrender.com")
    SWAGGER_SCHEMES = ["https"]


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    APP_HOST = os.getenv("APP_HOST", "127.0.0.1:5000")
    SWAGGER_SCHEMES = ["http"]
