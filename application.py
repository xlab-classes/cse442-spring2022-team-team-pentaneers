import json
from queue import Empty
from typing import List
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request, redirect, url_for, render_template, flash, session
import config
from Survey.Retrieve import RetrievePublicSurveys, RetrieveSurveyById, RetrieveSurveyResults, RetrieveUserSurveys, RetrieveSurveyForResponse 
from Survey.Delete import Delete
from Survey.Create import Survey, Response
from User import Account
from Survey.Update import ModifySurvey
from db_initial import initial, drop
from forms import RegistrationForm, LoginForm
from werkzeug.security import check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
import db_connector
from datetime import timedelta, date


app = Flask(__name__)
app.config.from_pyfile('config.py')

# IMPORTANT: Set to environment variable!
app.config['SECRET_KEY'] = config.SECRET_KEY
# When a user closes thr browser or tab, they must re-login
app.config['REMEMBER_COOKIE_SESSION'] = timedelta(seconds=0.01)
# Flask_Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"


# Login manager, deals with making sure the user gets loaded in correctly
@login_manager.user_loader
def load_user(id):
    print("id is: ", id)
    # connect database
    mydb = db_connector.dbConnector()
    mycursor = mydb.cursor()
    # select user_id
    sql = "select * from Users where id=%s"
    val = (id,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    print("Line 41: ", myresult[0][0])
    if len(myresult) > 0:
        return User(myresult[0][0])
    else:
        return myresult
                

##------------------The path to our homepage-----------------------
@app.route("/")
def home():
    return render_template('Homepage.html', title = "Homepage")

#------------------The path our survey creation page-----------------------

@app.route("/submitSurvey", methods=['GET', 'POST'])
@login_required
def createSurvey():
    data=json.loads(request.get_data(as_text=True))
    data = request.get_json('survey_data')
    print(data)
    id=Survey.survey(data)

    return json.dumps(id)


#------------------The path our signup page-----------------------
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']
        print("The form was validated")
        user_data = {'email': email, 'password': password, 'login': False, 'signup': True}
        
        # Grab all of the users that have the email address that was typed into the Register form and return the first one, None if none exist
        check_user = Account.account(user_data)
        # If there isn't already a user with the email, add it to the database
        if check_user != "account exists":
            # Create a new user to add to the Database
            flash(f"Account created for {email}!", 'Success')
            email = form.email.data
            # Clearing the form
            form.email.data = ''
            return redirect(url_for('home'))
        else:
            flash(f"That account already exists.", 'Error')
            email = form.email.data
            return redirect(url_for('signup'))


    return render_template('Signup.html', title = "Sign up", form = form)

    
#------------------The path to our login page-----------------------
@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']
        user_data = {'email': email, 'password': password, 'login': True, 'signup': False}
        check_user = Account.account(user_data)
        print("check user: ", check_user)
        if check_user == "account exists":
            user = User(email)
            if check_password_hash(user.get_password(email), password):
                login_user(user)
                session['email'] = email
                session['id'] = user.get_id()
                flash(f"Welcome Back {email}!", 'Success')
                return redirect(url_for('user_homepage'))
            
    
    if len(form.errors) != 0:
        flash(f"Please enter a valid email and password.", 'Error')
        return redirect(url_for('login'))

    return render_template('Login.html', title = "Login", form = form)

# ------------------Path to logout--------------------------------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    print("User has logged out")
    return redirect('/')

#------------------The path to our user homepage-----------------------
@app.route("/user_homepage")
@login_required
def user_homepage():
    return render_template('User_Homepage.html', title = "User Homepage")

#------------------The path to the view survey page-----------------------
@app.route("/view_surveys")
@login_required
def view_surveys():
    return render_template('View_Surveys.html', title = "View Surveys")

#------------------The path to the survey editor page-----------------------
@app.route("/survey_editor", methods=['GET', 'POST'])
@login_required
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
# @login_required
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
@login_required
def retrieveSurveyForResponse(survey_id):
    survey = RetrieveSurveyForResponse.retrieveSurveyForResponse(survey_id)
    return str(survey)


@app.route('/retrieve/survey/<email>/<survey_id>', methods = ['GET'])
@login_required
def retrieveSurveyById(survey_id, email):
    user_survey = RetrieveSurveyById.retrieveSurveyById(survey_id, email)
    return str(user_survey)


@app.route("/survey/modify/<id>", methods = ['PUT'])
@login_required
def modifySurvey(id):
    # Add user validation later

    # Data that contains any updated information
    data = json.loads(request.get_data(as_text=True))
    modified_survey = ModifySurvey.modifySurvey(id, data)
    return str(modified_survey)


@app.route("/survey/delete/<email>/<id>", methods = ['DELETE'])
@login_required
def deleteSurvey(email, id):
    deleted_surveys = Delete.deleteSurvey(email, id)
    return deleted_surveys


# Invalid path.
@app.route("/<error>")
def error(error):
    return f"page '{error}' does not exist!"

# User class
class User(UserMixin):
    user_email = ''
    def __init__(self, email):
        self.email = email

    def get_password(self, email):
        # connect database
        mydb = db_connector.dbConnector()
        mycursor = mydb.cursor()
        # select user_id
        sql = "select password from Users where email=%s"
        val = (self.email,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        mydb.close()
        mydb.close()
        if len(myresult) > 0:
            return myresult[0][0]

    def is_active(self):
        # connect database
        mydb = db_connector.dbConnector()
        mycursor = mydb.cursor()
        # select user_id
        sql = "select id from Users where email=%s"
        val = (self.email,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        mydb.close()
        if len(myresult) > 0:
            return True
        else:
            return False

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        # connect database
        mydb = db_connector.dbConnector()
        mycursor = mydb.cursor()
        # select user_id
        sql = "select id from Users where email=%s"
        val = (self.email,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        mydb.close()
        if len(myresult) > 0:
            return True
        else:
            return False
    
    def get_id(self):
        print(self.email)
        # connect database
        mydb = db_connector.dbConnector()
        mycursor = mydb.cursor()
        # select user_id
        sql = "select id from Users where email=%s"
        val = (self.email,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        print("in User class: ", myresult)
        mydb.close()
        if len(myresult) > 0:
            return myresult[0][0]

     

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
    app.run(debug = True) # Set to false for production
