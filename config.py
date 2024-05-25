import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://iameych77:Budzz5510~!@localhost:5432/cocktail_database')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
