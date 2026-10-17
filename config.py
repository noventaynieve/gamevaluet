import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave_secreta_gamevault_2026')
    
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '1234')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_NAME = os.environ.get('DB_NAME', 'gamevault_db')
    
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
