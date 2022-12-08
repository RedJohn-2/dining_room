from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:@localhost/dining_room?auth_plugin=mysql_native_password"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False # Autocommit
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'we4fh%gC_za:*8G5v=fbv'


app = Flask(__name__)
app.config.from_object(Config())
db = SQLAlchemy(app=app, session_options={'autoflush': False})
