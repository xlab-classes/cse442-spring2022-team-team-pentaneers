import datetime
import email
import json
from typing import List
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request
import mysql.connector
from datetime import date
import db_connector
import config
from Survey.Retrieve import RetrievePublicSurveys, RetrieveSurveyById, RetrieveSurveyResults, RetrieveUserSurveys, RetrieveSurveyForResponse 
from Survey.Delete import Delete
from Survey.Create import Survey, Response
from User import Account
from Survey.Update import ModifySurvey


app = Flask(__name__)
app.config.from_pyfile('config.py')

# IMPORTANT: Set to environment variable!
app.config['SECRET_KEY'] = config.SECRET_KEY

# Adding in UB's MYSQL Database (Make sure to change the formatting)


# Initialize the database
#Database = SQLAlchemy(app)


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

#path to create Surveys
@app.route("/submitSurvey", methods=['POST'])
def createSurvey():
    #print("hi!!!")
    data=json.loads(request.get_data(as_text=True))
    #print(data)
    id=Survey.survey(data)
    #print(id)
    return json.dumps(id)


#path to create account
@app.route("/signup", methods=['POST'])
def createAccount():
    data=json.loads(request.get_data(as_text=True))
    returnid=Account.account(data)
    return returnid



#path to create response
@app.route("/submitResponse", methods=['POST'])
def createResponse():
    data=json.loads(request.get_data(as_text=True))
    survey_id=Response.response(data)
    return survey_id



@app.route("/retrieve/userSurveys/<email>", methods=['GET'])
#User must be logged in, and must also be retreiving their own surveys

# Retrieve all surveys created by the user by their EMAIL
def retrieveSurveysUsers(email):
    retrieve = RetrieveUserSurveys.retrieveSurveysUsers(email)
    return str(retrieve)
    


@app.route("/retrieve/survey/<email>/<surveys_id>/results", methods=['GET'])
#User must be logged in, and must also be retreiving data on their own surveys

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




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
    app.run(debug = True) # Set to false for production
