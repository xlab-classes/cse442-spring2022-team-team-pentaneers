import datetime
import email
import json
from typing import List
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request, redirect, url_for, render_template, flash
import mysql.connector
from datetime import date
import db_connector
import config
from Survey.Retrieve import RetrievePublicSurveys, RetrieveSurveyById, RetrieveSurveyResults, RetrieveUserSurveys, RetrieveSurveyForResponse 
from Survey.Delete import Delete
from Survey.Create import Survey, Response
from User import Account
from Survey.Update import ModifySurvey
from db_initial import initial
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config.from_pyfile('config.py')

# IMPORTANT: Set to environment variable!
app.config['SECRET_KEY'] = config.SECRET_KEY

##------------------The path to our homepage-----------------------
@app.route("/")
def home():
    # initial()
    return render_template('Homepage.html', title = "Homepage")

##------------------The path our survey creation page-----------------------
@app.route("/submitSurvey", methods=['POST'])
def createSurvey():
    #print("hi!!!")
    data=json.loads(request.get_data(as_text=True))
    #print(data)
    id=Survey.survey(data)
    #print(id)
    return json.dumps(id)

##------------------The path to our signup page-----------------------
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    # if form.validate_on_submit():
        # email = request.form['email']; print("This is the email: ", email)
        # password = request.form['password']; print("This is the password: ", password)
        # print("The form was validated")
        # user_data = "{'email': {}, 'password': {}}".format(form.email.data, form.password.data)
        # data = json.loads(user_data)
        # # Grab all of the users that have the email address that was typed into the Register form and return the first one, None if non exist
        # check_user = Account.account(data)
        # # If there isn't already a user with the email, add it to the database
        # if check_user != "account exists":
        #     # Create a new user to add to the Database
        #     flash(f'Account created for {form.email.data}!', 'Success')
        #     email = form.email.data
        #     #Clearing the form
        #     form.email.data = ''
        #     return redirect(url_for('home'))
    #print(form.errors)
    return render_template('Signup.html', title = "Sign up", form = form)
    
#------------------The path to our login page-----------------------
@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('Login.html', title = "Login", form = form)

#------------------The path to our user homepage-----------------------
@app.route("/user_homepage")
def user_homepage():
    return render_template('User_Homepage.html', title = "User Homepage")

#------------------The path to the view survey page-----------------------
@app.route("/view_surveys")
def view_surveys():
    return render_template('View_Surveys.html', title = "View Surveys")

#------------------The path to the survey editor page-----------------------
@app.route("/survey_editor", methods=['GET', 'POST'])
def survey_editor():
    return render_template('Survey_Editor.html', title = "Survey Editor")

##------------------The path to our survey response page-----------------------
@app.route("/submitResponse", methods=['POST'])
def createResponse():
    data=json.loads(request.get_data(as_text=True))
    survey_id=Response.response(data)
    return survey_id



@app.route("/retrieve/userSurveys/<email>", methods=['GET'])
# User must be logged in, and must also be retreiving their own surveys
# Retrieve all surveys created by the user by their EMAIL
def retrieveSurveysUsers(email):
    retrieve = RetrieveUserSurveys.retrieveSurveysUsers(email)
    return str(retrieve)


@app.route("/retrieve/survey/<email>/<surveys_id>/results", methods=['GET'])
# User must be logged in, and must also be retreiving data on their own surveys
# Retrieve specific survey results
def retrieveSurveyResults(email, surveys_id):
    survey_results = RetrieveSurveyResults.retrieveSurveyResults(email, surveys_id)
    return str(survey_results)


@app.route('/retrieve/PublicSurveys')
# User does NOT have to be logged in to see public surveys
def retrievePublicSurveys():
    all_surveys = RetrievePublicSurveys.retrievePublicSurveys()
    
    return str(all_surveys)


@app.route('/survey/form/<survey_id>', methods = ['GET'])
def retrieveSurveyForResponse(survey_id):
    survey = RetrieveSurveyForResponse.retrieveSurveyForResponse(survey_id)
    return str(survey)


@app.route('/retrieve/survey/<email>/<survey_id>', methods = ['GET'])
def retrieveSurveyById(survey_id, email):
    user_survey = RetrieveSurveyById.retrieveSurveyById(survey_id, email)
    return str(user_survey)


@app.route("/survey/modify/<id>", methods = ['PUT'])
# User must be logged in, and the Sruvey must belong to him
def modifySurvey(id):
    # Add user validation later

    # Data that contains any updated information
    data = json.loads(request.get_data(as_text=True))
    modified_survey = ModifySurvey.modifySurvey(id, data)
    return str(modified_survey)


@app.route("/survey/delete/<email>/<id>", methods = ['DELETE'])
def deleteSurvey(email, id):
    deleted_surveys = Delete.deleteSurvey(email, id)
    return deleted_surveys


# Invalid path.
@app.route("/<error>")
def error(error):
    return f"page '{error}' does not exist!"




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
    app.run(debug = True) # Set to false for production
