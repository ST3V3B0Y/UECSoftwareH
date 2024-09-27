import os
import secrets
SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(32))
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@127.0.0.1:3306/Disponibilidad_Equipos'
SQLALCHEMY_TRACK_MODIFICATIONS = False

#SERVER_HOST = '10.100.103.142'
SERVER_HOST = '172.20.14.154'
SERVER_PORT = 5000
#SERVER_PORT = 5040
