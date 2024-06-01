from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from disease_prediction.models import *
# from wtforms.ext.sqlalchemy.fields import QuerySelectField
# from wtforms import SelectField



class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login') 


class AddDoctorForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    image = FileField('Upload Photo', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    email = StringField('Email', validators=[DataRequired()])
    specialisation = StringField('Specialisation', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AddUserForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    age = StringField('Age',validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    place = StringField('Place', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')