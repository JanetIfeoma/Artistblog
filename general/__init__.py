from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os import path 

db =SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY'] ='4dbd2e68bf5f98122dd3e3341180c13d'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .display import display
    from .form import form

    app.register_blueprint(display, url_prefix="/")
    app.register_blueprint(form, url_prefix="/")

    from .models import User,Post

    create_database(app)

    lmanager =  LoginManager()
    lmanager.login_display = "form.login"
    lmanager.init_app(app)

    @lmanager.user_loader
    def load_user(id):
     return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists("general/" + DB_NAME):
       app.app_context().push()
       db.create_all()
    print("Database Created!!")
