import sys, os, inspect
import datetime
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
parent_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(1, parent_parent_dir)

from Survey.Retrieve.RetrieveSurveyForResponse import retrieveSurveyForResponse
from Survey.Create.Response import response
from Survey.Create.Survey import survey
from db_connector import dbConnector

def test():

    mydb = dbConnector()
    mycursor = mydb.cursor()

    #get current date,YYYY-MM-DD format
    created_date = datetime.date.today()

    survey_dict = {
        "email": "test@email.com",
        "title": "test1",
        "description":"test description 1",
        "questions":[['do you like cats?', 'Multiple Choice', ['yes', 'no']],
        ['why', 'Short Response', None],
        ['do you want to keep coding?', 'Multiple Choice', ['pain', 'wuyu']]],
        "expired_date": "2022-03-22",
        "visibility":"public"
        }
    
    retrieved_survey = survey(survey_dict)

    response_dict = {
        "email": "test@email.com", 
        "survey_id":1,
        "response":[
            ["Multiple Choice", 1],
            ["Short Response","test"],
            ["Multiple Choice", 1]
            ]
        }

    
    retrieved_response = response(response_dict)

    expected_outcome = ['test@email.com', 'test1', 'test description 1', 
    {'question_1': ['do you like cats?', 'Multiple Choice', ['yes', 'no']]},
    {'question_2': ['why', 'Short Response', None]}, 
    {'question_3': ['do you want to keep coding?', 'Multiple Choice', ['pain', 'wuyu']]}
    ]

    actual_outcome = retrieveSurveyForResponse(1)
    


    mycursor.execute('CREATE TABLE IF NOT EXISTS Surveys (id int AUTO_INCREMENT PRIMARY KEY, email varchar(255), title varchar(255) , description varchar(255), created_on DATE, expired_on Date, surveys_id int, visibility varchar(255))')
    mydb.commit()

    sql="Insert into Surveys (email, title, description, created_on, expired_on, surveys_id, visibility) values (%s,%s,%s,%s,%s,%s,%s)"
    email = "test@email.com"
    survey_title = "test title"
    survey_description = "test description"
    expired_date = None
    survey_id = 1
    visibility = 'public'

    val=(email, survey_title, survey_description, created_date, expired_date, survey_id, visibility)
    mycursor.execute(sql,val)
    mydb.commit()

    if str(expected_outcome) == actual_outcome:
        mycursor = mydb.cursor()
        sql = "DROP TABLE IF EXISTS Surveys"
        mycursor.execute(sql)
        sql = "DROP TABLE IF EXISTS Response"
        mycursor.execute(sql)
        sql = "DROP TABLE IF EXISTS Questions"
        mycursor.execute(sql)
        sql = "DROP TABLE IF EXISTS Survey_Questions"
        mycursor.execute(sql)
        mycursor.close()
        return "Passed!"
    else:
        mycursor = mydb.cursor()
        sql = "DROP TABLE IF EXISTS Surveys"
        mycursor.execute(sql)
        sql = "DROP TABLE IF EXISTS Response"
        mycursor.execute(sql)
        sql = "DROP TABLE IF EXISTS Questions"
        mycursor.execute(sql)
        sql = "DROP TABLE IF EXISTS Survey_Questions"
        mycursor.execute(sql)
        mycursor.close()
        return "Failed!"


