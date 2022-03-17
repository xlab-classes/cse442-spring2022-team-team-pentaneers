from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

# This contains every field on the Signup page. 
# It will validate certain user inputs.
class RegistrationForm(FlaskForm):
    #firstName = StringField('First Name', validators = [DataRequired(), Length(min = 2, max = 30)])
    #lastName = StringField('Last Name', validators = [DataRequired(), Length(min = 2, max = 30)])

    email = StringField('Email', validators = [DataRequired(), Email()])

    password = PasswordField('Password', validators = [DataRequired(), Length(min = 5, max = 30), EqualTo('confirm_password', message="Passwords must match")])

    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

# This contains every field on the Login page.
# It will validate certain user inputs.
class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])

    password = PasswordField('Password', validators = [DataRequired(), Length(min = 5, max = 30)])
    
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')