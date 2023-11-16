import os
#SECRET_KEY = os.urandom(32)
SECRET_KEY = os.environ['SECRET_KEY']
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False
