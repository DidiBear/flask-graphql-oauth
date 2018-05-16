import os

DEBUG       = os.environ.get('DEBUG',       True)
HOSTNAME    = os.environ.get('HOSTNAME',    '0.0.0.0')
PORT        = os.environ.get('PORT',        5000)

# SERVER_NAME = f"{HOSTNAME}:{PORT}"

SECRET_KEY  = 'itsatrap'
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True