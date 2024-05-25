import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'd8a1831f73e59c8a41271e8560ef28df')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgres://iameych77:Zkic3xh6o6rNpxqetnb78xdVh3uxG16y@dpg-cp7mv4md3nmc73buv780-a/cocktail_database_lw3l')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
