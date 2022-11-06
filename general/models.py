from . import db 
from flask_login import UserMixin
from  sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email= db.Column(db.String(120), nullable=False, unique= True)
    date_created = db.Column(db.DateTime(timezone=True), default= func.now())
    posts =db.relationship('Post', backref='user', passive_deletes= True)
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id', on_delete="CASCADE"),nullable=False) 
    text= db.Column(db.Text(120), nullable=False)
    posted_on = db.Column(db.DateTime(timezone=True), default= func.now())