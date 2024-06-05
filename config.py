import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'd8a1831f73e59c8a41271e8560ef28df')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application. Did you forget to set it?")
    
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgres://iameych77:Zkic3xh6o6rNpxqetnb78xdVh3uxG16y@dpg-cp7mv4md3nmc73buv780-a/cocktail_database_lw3l')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("No DATABASE_URL set for Flask application. Did you forget to set it?")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
