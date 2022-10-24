import os

BASE_DIR = os.path.dirname(os.path.abspath(__name__))
IMG_FOLDER = os.path.join('static', 'pics')


class Config:
    DEBUG = True 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'database.db') # muuta tää vielä jotenkin ettei tallennu kahteen paikkaan
    SECRET_KEY='dev'
    FLASK_ADMIN_SWATCH = 'cerulean'
    UPLOAD_FOLDER = IMG_FOLDER
    SECURITY_PASSWORD_SALT = '\x99\t\x1c:BE\xf5\xaf\xf4@3\xef\xfd\x91\x9b\x00\xe8\n\x038\x1c\x07\x0c\x1e' # kato nää vielä mitä näihin pitää laittaa
    #SECURITY_PASSWORD_HASH = 'sha512_crypt'

    # Missä secret key ja security_password_salt pitää säilyttää? Environment variablena?