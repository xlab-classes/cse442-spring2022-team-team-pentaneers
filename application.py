import json
import time
from queue import Empty
from typing import List

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, redirect, url_for, render_template, flash, session
from flask import Flask,request, redirect, url_for, render_template, flash, session
from flask_cors import CORS
import config
from Survey.Retrieve import RetrievePublicSurveys, RetrieveSurveyById, RetrieveSurveyForResponseByString, \
    RetrieveSurveyResults, RetrieveUserSurveys, RetrieveSurveyForResponse, getSurveyID, getSurveyURL
from Survey.Retrieve import RetrievePublicSurveys, RetrieveSurveyById, RetrieveSurveyForResponseByString, RetrieveSurveyResults, RetrieveUserSurveys, RetrieveSurveyForResponse, getSurveyID, getSurveyURL
from Survey.Delete import Delete
from Survey.Create import Survey, Response
from Survey.Status import Auto, Close, Open, Private
from User import Account
from Survey.Update import ModifySurvey
from db_initial import initial, drop
from forms import RegistrationForm, LoginForm
from werkzeug.security import check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
import db_connector
from datetime import timedelta, date, datetime


from werkzeug.security import check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
import db_connector
from datetime import timedelta, date
import time


app = Flask(__name__)
app.config.from_pyfile('config.py')
cors = CORS(app)



# IMPORTANT: Set to environment variable!
app.config['SECRET_KEY'] = config.SECRET_KEY
# When a user closes thr browser or tab, they must re-login
app.config['REMEMBER_COOKIE_SESSION'] = timedelta(seconds=0.01)
# Flask_Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"

initial()

# Login manager, deals with making sure the user gets loaded in correctly
@login_manager.user_loader
def load_user(id):

    # connect database
    mydb = db_connector.dbConnector()
    mycursor = mydb.cursor()
    # select user_id
    sql = "select * from Users where id=%s"
    val = (id,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()

    if len(myresult) > 0:
        return User(myresult[0][0])
    else:
        return None


#------------------The path to our homepage-----------------------
@app.route("/")
def home():
    return render_template('Homepage.html', title = "Homepage")

#------------------The path our survey creation page-----------------------
@app.route("/submitSurvey", methods=['GET', 'POST'])
@login_required
def createSurvey():

    email = {'email': session['email']}
    data = request.get_json('survey_data')

    # Merging the logged in user with the incoming data to submit the survey properly
    data = {**email, **data}
    print(data)

    id=Survey.survey(data)
    surveys_id = getSurveyID.surveysID(session['email'], id)
    survey_url = getSurveyURL.get(session['email'], surveys_id)
    session['surveys_id'] = surveys_id

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


#------------------Path to logout--------------------------------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('id')
    session.pop('email')
    print("User has logged out")
    return redirect('/')

#------------------The path to our user homepage-----------------------
@app.route("/user_homepage")
@login_required
def user_homepage():
    return render_template('User_Homepage.html', title = "User Homepage")

#------------------The path to our user view survey page-----------------------
@app.route("/view_surveys", methods = ['POST', 'GET'])
@login_required
def view_surveys():
    print("This is the host url: ", request.host_url)
    email = session['email']

    surveys = retrieveSurveysUsers(email)

    # We want the titles of the surveys for that user.
    # They will be displayed on the user view survey page.

    count = len(surveys[1])
    num = 0
    titles = []
    URLlist = []

    while num != count:
        title = str(surveys[1][num].keys())
        title = title.split("'")
        titles += [title[1]]

        num = num + 1

        URL = getSurveyURL.get(session["email"], num)
        URLlist.append(URL)
    mindate = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    return render_template('View_Surveys.html', title = "View Surveys", titles = titles, URLlist = URLlist,mindate=mindate)


#------------------The path to the survey editor page-----------------------
@app.route("/survey_editor", methods=['GET', 'POST'])
@login_required
def survey_editor():
    mindate = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    print(mindate)
    mindate+="T00:00:00"
    return render_template('Survey_Editor.html', title="Survey Editor",mindate=mindate)

#------------------The path to our submit survey response page-----------------------
@app.route("/submitResponse", methods=['POST'])
def createResponse():
    data=json.loads(request.get_data(as_text=True))
    survey_id=Response.response(data)
    return survey_id

#------------------The path to the view survey responses page-----------------------
@app.route("/survey_responses/<surveys_id>", methods=['GET', 'POST'])
@login_required
def survey_responses(surveys_id):

    email = session['email']
    survey_id = getSurveyID.surveyID(email, surveys_id)

    results = retrieveSurveyResults(session['email'], surveys_id)
    survey_info = retrieveSurveyForResponse(survey_id)

    #print("The survey information is: ", survey_info, type(survey_info))
    #print("The results are: ", results, type(results))

    survey_title = survey_info[1]
    survey_description = survey_info[2]

    # First three indexes are the email, title, and description

    # MC section
    questions = results[0][0]
    options = results[0][1]
    responses = results[0][2]
    total_num_of_responses = results[2]

    # SA section
    questionsSA = results[1][0]
    responsesSA = results[1][1]

    percent_values = []

    for response in responses:
        response_percentages = []
        for number in response:
            if number != 0:
                decimal_number = number/total_num_of_responses
            else:
                decimal_number = 0
            percentage = "{:.0%}".format(decimal_number)
            response_percentages.append(percentage)
        percent_values.append(response_percentages)

    print(percent_values)

    return render_template('Survey_Responses.html', title = "Survey Responses", questions = questions, options = options,
    total_num_of_responses = total_num_of_responses, survey_title = survey_title, survey_description = survey_description,
    percent_values = percent_values, questionsSA = questionsSA, responsesSA = responsesSA)


#------------------The path to our survey creation success page-----------------------
@app.route("/creation_success", methods=['POST', 'GET'])
@login_required
def creation_success():
    time.sleep(0.10)
    get_latest_surveys_id = getSurveyID.latestSurveysID(session['email'])
    URL = getSurveyURL.get(session["email"], get_latest_surveys_id)

    return render_template('Creation_Completion.html', title = "Survey Creation Success", URL = URL)


#------------------The path to our survey answer submission success page-----------------------
@app.route("/submission_success", methods=['POST', 'GET'])
def submission_success():
    return render_template('Answer_Completion.html', title = "Survey Submission Success")

#------------------The path to our survey answer submission success page-----------------------
@app.route("/deleted_survey", methods=['POST', 'GET'])
def deleted_survey():
    return render_template('Deleted_Survey.html', title = "Deleted Survey")


#------------------The path that will delete a survey-----------------------
@app.route('/delete', methods = ['DELETE', 'POST', 'GET'])
@login_required
def delete_survey():

    email = session['email']
    data = request.get_json('data')

    print("OK means delete the survey, cancel means DON'T delete the survey: ", data)

    # OK means delete the survey, cancel means DON'T delete the survey
    delete_option = data.split(" ")
    surveys_id = delete_option[1]

    if delete_option[0] == "OK":
        # We can delete the survey.
        survey_id = getSurveyID.surveyID(email, surveys_id)
        deleteSurvey(email, survey_id)


    return redirect(url_for('view_surveys'))

@app.route("/retrieve/userSurveys/<email>", methods=['GET'])
@login_required
# User must be logged in, and must also be retreiving their own surveys
# Retrieve all surveys created by the user by their EMAIL
def retrieveSurveysUsers(email):
    retrieve = RetrieveUserSurveys.retrieveSurveysUsers(email)
    return retrieve


@app.route("/retrieve/survey/<email>/<surveys_id>/results", methods=['GET'])
@login_required
# Retrieve specific survey results
def retrieveSurveyResults(email, surveys_id):
    survey_results = RetrieveSurveyResults.retrieveSurveyResults(email, surveys_id)
    return survey_results


@app.route('/retrieve/PublicSurveys')
# User does NOT have to be logged in to see public surveys
def retrievePublicSurveys():
    all_surveys = RetrievePublicSurveys.retrievePublicSurveys()
    if all_surveys == None:
        return "There are no public surveys available yet!"
    
    return all_surveys


@app.route('/survey/form/<survey_id>', methods = ['GET'])
def retrieveSurveyForResponse(survey_id):
    survey = RetrieveSurveyForResponse.retrieveSurveyForResponse(survey_id)
    return survey

@app.route('/survey/respond/<surveys_id>/<unique_string>', methods = ['GET'])
def respondToSurveyWithURL(surveys_id, unique_string):
    authenticated = False
    if 'email' in session.keys():
        authenticated = True
    survey = RetrieveSurveyForResponseByString.retrieve(surveys_id, unique_string)
    print(str(survey))
    if survey == None:
        return render_template('Deleted_Survey.html', title = "Deleted Survey", authenticated = authenticated)

    print(survey[0])
    t = survey[0]
    if type(survey[1]) == str:
        d = survey[1]
    else:
        q = survey[1]
    file = open('Rendered_Survey.html', 'w')
    # html_form = """<form action="/action_page.php">
    #         <label for="cars">Choose a car:</label>
    #         <select name="cars" id="cars" multiple>
    #             <option value="volvo">Volvo</option>
    #             <option value="saab">Saab</option>
    #             <option value="opel">Opel</option>
    #             <option value="audi">Audi</option>
    #         </select>
    #         <br><br>
    #         <input type="submit" value="Submit">
    #         </form>"""
    # file.write(html_form)
    file.close()
    q = survey[2]['question_1'][1]
    return render_template('Survey_Answering_Page.html', title = t, description = d, question = q)


@app.route('/retrieve/survey/<email>/<survey_id>', methods = ['GET'])
@login_required
def retrieveSurveyById(survey_id, email):
    user_survey = RetrieveSurveyById.retrieveSurveyById(survey_id, email)
    return user_survey


@app.route("/survey/modify/<id>", methods = ['PUT'])
@login_required
def modifySurvey(id):
    # Add user validation later

    # Data that contains any updated information
    data = json.loads(request.get_data(as_text=True))
    modified_survey = ModifySurvey.modifySurvey(id, data)
    return modified_survey


@app.route("/survey/delete/<email>/<id>", methods = ['DELETE'])
@login_required
def deleteSurvey(email, id):
    deleted_surveys = Delete.deleteSurvey(email, id)
    return deleted_surveys

# Path to drop all of the tables in the Database
@app.route("/clear/database/<ubid>")
def clearDatabase(ubid):
    if ubid in config.UBITS:
        drop()
        initial()
    return render_template('Homepage.html', title = "Homepage")

@app.route("/survey/private/<survey_id>", methods = ['PUT'])
@login_required
def private(survey_id):
    email = session['email']
    survey=Private.closeSurvey(survey_id,email)
    return "success"

@app.route("/survey/open/<survey_id>", methods = ['PUT'])
@login_required
def reopen(survey_id):
    email = session['email']
    survey = Open.openSurvey(survey_id,email)
    return "success"

@app.route("/survey/close/<survey_id>", methods = ['PUT'])
@login_required
def close(survey_id):
    email = session['email']
    survey = Close.closeSurvey(survey_id,email)
    return "The Survey that you are attempting to answer has been closed!"

# Invalid path.
@app.route("/<error>")
def error(error):
    return f"page '{error}' does not exist!"


@app.route("/getlink/<surveys_id>")
def getlink(surveys_id):
    email = session['email']
    result=getSurveyURL.get(email,surveys_id)
    print("result")
    print(result)
    return result
    pass


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
    app.run(host='0.0.0.0', port=8000, debug=True)
    #app.run() # Set to false for production
