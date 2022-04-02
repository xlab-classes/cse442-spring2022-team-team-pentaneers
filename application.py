import json
from queue import Empty
from typing import List
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request, redirect, url_for, render_template, flash, jsonify
from flask_cors import CORS
import config
from Survey.Retrieve import RetrievePublicSurveys, RetrieveSurveyById, RetrieveSurveyResults, RetrieveUserSurveys, RetrieveSurveyForResponse 
from Survey.Delete import Delete
from Survey.Create import Survey, Response
from User import Account
from Survey.Update import ModifySurvey
from db_initial import initial, drop
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config.from_pyfile('config.py')
cors = CORS(app)

# IMPORTANT: Set to environment variable!
app.config['SECRET_KEY'] = config.SECRET_KEY

#------------------The path to our homepage-----------------------
@app.route("/")
def home():
    return render_template('Homepage.html', title = "Homepage")

#------------------The path our survey creation page-----------------------
@app.route("/submitSurvey", methods=['POST'])
def createSurvey():
    data=json.loads(request.get_data(as_text=True))
    
    id=Survey.survey(data)
    
    return json.dumps(id)


#------------------The path our signup page-----------------------
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    print(form.email.data)
    print(form.password.data)
    print(form.confirm_password.data)
    print(form.validate_on_submit())
    if form.validate_on_submit():
        email = request.form['email']; print("This is the email: ", email)
        password = request.form['password']; print("This is the password: ", password)
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
            #Clearing the form
            form.email.data = ''
            return redirect(url_for('signup'))


    return render_template('Signup.html', title = "Sign up", form = form)

    
#------------------The path to our login page-----------------------
@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form['email']; print("This is the email: ", email)
        password = request.form['password']; print("This is the password: ", password)
        user_data = {'email': email, 'password': password, 'login': True, 'signup': False}
        check_user = Account.account(user_data)
        print("check user: ", check_user)
        if check_user == "account exists":
            flash(f"Welcome Back {email}!", 'Success')
            # Clearing the form
            #form.email.data = ''
            return redirect(url_for('user_homepage'))
        else:
            flash(f"Incorrect email or password.", 'Error')
            return redirect(url_for('login'))
    
    if len(form.errors) != 0:
        flash(f"Please enter a valid email and password.", 'Error')
        return redirect(url_for('login'))

    return render_template('Login.html', title = "Login", form = form)


#------------------The path to our user homepage-----------------------
@app.route("/user_homepage")
def user_homepage():
    return render_template('User_Homepage.html', title = "User Homepage")

#------------------The path to our user view survey page-----------------------
@app.route("/view_surveys")
def view_surveys():

    # Hardcode email for now
    surveys = retrieveSurveysUsers("test@gmail.com")
    #print(surveys)

    # We want the title

    count = len(surveys[1])
    num = 0
    titles = []

    while num != count:
        #print(surveys[1][num].keys())
        title = str(surveys[1][num].keys())

        title = title.split("'")
        #print(title[1])
        titles += [title[1]]

        num = num + 1

    print("The titles are: ", titles)
    return render_template('View_Surveys.html', title = "View Surveys", titles = titles)

#------------------The path to the survey editor page-----------------------
@app.route("/survey_editor", methods=['GET', 'POST'])
def survey_editor():
    return render_template('Survey_Editor.html', title = "Survey Editor")

#------------------The path to our submit survey response page-----------------------
@app.route("/submitResponse", methods=['POST'])
def createResponse():
    data=json.loads(request.get_data(as_text=True))
    survey_id=Response.response(data)
    return survey_id

#------------------The path to the view survey responses page-----------------------
@app.route("/survey_responses", methods=['GET', 'POST'])
def survey_responses():

    # Assuming all multiple choice for now
    # Hard code email and surveys_id for now
    results = retrieveSurveyResults("test@gmail.com", 1)
    survey_info = retrieveSurveyForResponse(1)

    print("The survey information is: ", survey_info, type(survey_info))
    print("The results are: ", results, type(results))

    survey_title = survey_info[1]
    survey_description = survey_info[2]

    # First three indexes are the email, title, and description
    number_questions = (len(survey_info)) - 3
    question_num = 0
    index = 3
    print("The number of questions is: ", number_questions)

    while index != len(survey_info):
        survey_info[int(index)]['question_' + str(question_num + 1)]
        print(survey_info[int(index)]['question_' + str(question_num + 1)])

        index = index + 1
        question_num = question_num + 1


    return render_template('Survey_Responses.html', title = "Survey Responses", results = json.dumps(results), 
    survey_title = survey_title, survey_description = survey_description)




@app.route("/retrieve/userSurveys/<email>", methods=['GET'])
# User must be logged in, and must also be retreiving their own surveys
# Retrieve all surveys created by the user by their EMAIL
def retrieveSurveysUsers(email):
    retrieve = RetrieveUserSurveys.retrieveSurveysUsers(email)
    return retrieve


@app.route("/retrieve/survey/<email>/<surveys_id>/results", methods=['GET'])
# User must be logged in, and must also be retreiving data on their own surveys
# Retrieve specific survey results
def retrieveSurveyResults(email, surveys_id):
    survey_results = RetrieveSurveyResults.retrieveSurveyResults(email, surveys_id)
    return survey_results


@app.route('/retrieve/PublicSurveys')
# User does NOT have to be logged in to see public surveys
def retrievePublicSurveys():
    all_surveys = RetrievePublicSurveys.retrievePublicSurveys()
    
    return all_surveys


@app.route('/survey/form/<survey_id>', methods = ['GET'])
def retrieveSurveyForResponse(survey_id):
    survey = RetrieveSurveyForResponse.retrieveSurveyForResponse(survey_id)
    return survey


@app.route('/retrieve/survey/<email>/<survey_id>', methods = ['GET'])
def retrieveSurveyById(survey_id, email):
    user_survey = RetrieveSurveyById.retrieveSurveyById(survey_id, email)
    return user_survey


@app.route("/survey/modify/<id>", methods = ['PUT'])
# User must be logged in, and the Survey must belong to him
def modifySurvey(id):
    # Add user validation later

    # Data that contains any updated information
    data = json.loads(request.get_data(as_text=True))
    modified_survey = ModifySurvey.modifySurvey(id, data)
    return modified_survey


@app.route("/survey/delete/<email>/<id>", methods = ['DELETE'])
def deleteSurvey(email, id):
    deleted_surveys = Delete.deleteSurvey(email, id)
    return deleted_surveys

@app.route("/survey_data", methods=['GET', 'POST'])
def view():
    survey_data = request.get_json('survey_data')
    survey_data = jsonify(survey_data)#[title, description, question_list, question_type, mc_option_list]
    s_title = survey_data[0]
    s_description = survey_data[1]
    s_question_list = survey_data[2]
    # s_question_type = survey_data[3]
    # s_mc_option_list = survey_data[4]
    parsed_data = {'title': s_title, 'description':s_description, 'questions': s_question_list, 'expired_date': '2021-03-22', 'visibility': 'Public'}
    createSurvey(parsed_data)
    return survey_data


# Invalid path.
@app.route("/<error>")
def error(error):
    return f"page '{error}' does not exist!"




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
    app.run(debug = True) # Set to false for production
