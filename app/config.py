import os

BASE_DIR = os.path.dirname(os.path.abspath(__name__))
IMG_FOLDER = os.path.join('static', 'pics')

class Config:
    DEBUG = True 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'database.db') # muuta tää vielä jotenkin ettei tallennu kahteen paikkaan
    SECRET_KEY='dev'
    FLASK_ADMIN_SWATCH = 'cerulean'
    UPLOAD_FOLDER = IMG_FOLDER