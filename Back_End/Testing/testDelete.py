import sys, os, inspect
import datetime
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
parent_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(1, parent_parent_dir)

from Delete.Delete import deleteSurvey
from create.Response import response
from create.Survey import survey
from db_connector import dbConnector

def test():
    # Connecting to the database
    mydb = dbConnector("root")
    mycursor = mydb.cursor()

    #---------Submitting to a Survey Manually----------------#
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

    submit_survey = survey(survey_dict)

    #---------Responding to a Survey Manually----------------#
    response_dict = {
        "email": "test@email.com", 
        "survey_id":1,
        "response":[
            ["Multiple Choice", 1],
            ["Short Response","test"],
            ["Multiple Choice", 1]
            ]
        }

    
    submit_response = response(response_dict)

    response_dict_2 = {
        "email": "lol@email.com", 
        "survey_id":1,
        "response":[
            ["Multiple Choice", 2],
            ["Short Response","test2"],
            ["Multiple Choice", 2]
            ]
        }

    submit_response_2 = response(response_dict_2)

    expected_outcome = "Survey has been deleted for email: test@email.com with survey_id = 1"

    # Call the function we're testing to see if returned what we wanted
    actual_outcome = deleteSurvey('test@email.com', 1)

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

print(test())
