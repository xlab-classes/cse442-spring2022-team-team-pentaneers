from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, InputRequired

# This contains every field on the Signup page. 
# It will validate certain user inputs.
class RegistrationForm(FlaskForm):
    #firstName = StringField('First Name', validators = [DataRequired(), Length(min = 2, max = 30)])
    #lastName = StringField('Last Name', validators = [DataRequired(), Length(min = 2, max = 30)])

    email = StringField('Email', validators = [InputRequired(message="An Email is required!"), DataRequired(), Email(message="Not a valid email")])

    password = PasswordField('Password', validators = [InputRequired(message="A password is required!"), DataRequired(message="Please enter a password"), Length(min = 5, max = 32, message="Password must be between 5 and 32 characters")])

    confirm_password = PasswordField('Confirm Password', validators = [InputRequired(message="You must enter a matching password!"), DataRequired(), EqualTo('password', message="Passwords must match")])

    submit = SubmitField('Sign Up')

# This contains every field on the Login page.
# It will validate certain user inputs.
class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])

    password = PasswordField('Password', validators = [DataRequired(), Length(min = 5, max = 32)])
    
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')