from main import db, login
import sqlalchemy
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

class Listing(db.Model):
    """
    Hold all types of data on listing.
    """
    __tablename__ = 'listings'

    id = db.Column(db.Integer , primary_key = True)
    link = db.Column(db.String(400), unique = True) #'url' for both Indeed and Craigslist
    created = db.Column(db.String(400)) #'date' for Indeed and 'datetime' for Craigslist
    name = db.Column(db.String(400),nullable = True) #'company' Name Only for Indeed
    title = db.Column(db.String(400)) # 'jobtitle' for Indeed and and 'name' forCraigslist
    location = db.Column(db.String(400)) #'formattedLocation', and 'where' for craigslist
    city = db.Column(db.String(400)) #Los Angeles or New York
    JobKeyOrID = db.Column(db.String(400), unique=True) #'jobkey' for Indeed and 'id' for Craigslist
    InorCl = db.Column(db.String(400))

class Settings(UserMixin,db.Model):
    """
    Hold all settings which can be changed on webapp
    """
    __tablename__="settings"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(400))
    password_hash = db.Column(db.String(128))
    indeed =  db.Column(db.Boolean,default=True)
    craigslist =  db.Column(db.Boolean,default=True)
    indeedListings = db.relationship('indeedModel',backref='author',lazy='dynamic')
    clListings = db.relationship('craigslistModel',backref='author',lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return Settings.query.get(int(id))

class indeedModel(db.Model):
    __tablename__="indeedModel"
    id = db.Column(db.Integer,primary_key=True)
    city = db.Column(db.String(400))
    keyword = db.Column(db.String(400))
    slackChannel = db.Column(db.String(400))
    user_id = db.Column(db.Integer,db.ForeignKey('settings.id'))

class craigslistModel(db.Model):
    __tablename__="craigslistModel"
    id = db.Column(db.Integer,primary_key=True)
    city = db.Column(db.String(400))
    area = db.Column(db.String(400))
    category = db.Column(db.String(400))
    internship = db.Column(db.Boolean)
    slackChannel = db.Column(db.String(400))
    user_id = db.Column(db.Integer,db.ForeignKey('settings.id'))
