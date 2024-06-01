from disease_prediction import db,app,login_manager
from flask_login import UserMixin
from flask_table import Table, Col, LinkCol
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(id):
    return Login.query.get(int(id))



class Login(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80), nullable=False)
    usertype = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(200))
    contact = db.Column(db.String(200))




class Doctor(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    email = db.Column(db.String(200))
    specialisation = db.Column(db.String(200))
    department = db.Column(db.String(200))
    contact = db.Column(db.String(200))
    password = db.Column(db.String(200))


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    age = db.Column(db.String(200))
    gender = db.Column(db.String(200))
    address = db.Column(db.String(200))
    place = db.Column(db.String(200))
    email = db.Column(db.String(200))
    contact = db.Column(db.String(200))
    password = db.Column(db.String(200))





class Feedback(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    email= db.Column(db.VARCHAR)
    phone= db.Column(db.Integer)
    subject = db.Column(db.String(200))
    message= db.Column(db.String(200))




class DoctorFeedback(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    email= db.Column(db.VARCHAR)
    phone= db.Column(db.Integer)
    subject = db.Column(db.String(200))
    message= db.Column(db.String(200))
   
    


class User2(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    subject = db.Column(db.String(200))
    message= db.Column(db.String(200))
    reply=db.Column(db.String(200))



class User3(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    subject = db.Column(db.String(200))
    message= db.Column(db.String(200))
    reply=db.Column(db.String(200))