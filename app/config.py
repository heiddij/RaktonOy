import os
from decouple import config
from dotenv import load_dotenv
from os import environ, path

BASE_DIR = path.dirname(path.abspath(__name__))
IMG_FOLDER = path.join('static', 'pics')
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '../.env'))


class Config:
    DEBUG = True 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(BASE_DIR, 'instance', 'database.db') 
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_ADMIN_SWATCH = 'cerulean'
    UPLOAD_FOLDER = IMG_FOLDER
    SECURITY_PASSWORD_SALT = environ.get('SECURITY_PASSWORD_SALT') 
    #SECURITY_PASSWORD_HASH = 'sha512_crypt'