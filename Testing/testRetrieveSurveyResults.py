import sys, os, inspect
import datetime
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
parent_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(1, parent_parent_dir)

from Back_End.Retrieve.RetrieveSurveyResults import retrieveSurveyResults
from Back_End.create.Response import response
from Back_End.create.Survey import survey
from db_connector import dbConnector

def test():

    mydb = dbConnector()
    mycursor = mydb.cursor()

    #get current date,YYYY-MM-DD format
    created_date = datetime.date.today()

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

    retrieved_survey = survey(survey_dict)

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

    
    retrieved_response = response(response_dict)

    response_dict_2 = {
        "email": "lol@email.com", 
        "survey_id":1,
        "response":[
            ["Multiple Choice", 2],
            ["Short Response","test2"],
            ["Multiple Choice", 2]
            ]
        }

    retrieved_response_2 = response(response_dict_2)

    #--------------Checking for Expected Outcomes-------------------#
    expected_outcome = [
    ['test@email.com', {'question_number': 1, 'multiple_choice_response': 1}], 
    ['test@email.com', {'question_number': 2, 'short_answer_response': 'test'}],
    ['test@email.com', {'question_number': 3, 'multiple_choice_response': 1}],
    ['lol@email.com', {'question_number': 1, 'multiple_choice_response': 2}],
    ['lol@email.com', {'question_number': 2, 'short_answer_response': 'test2'}],
    ['lol@email.com', {'question_number': 3, 'multiple_choice_response': 2}]
    ]

    # Call the function we're testing to see if returned what we wanted
    actual_outcome = retrieveSurveyResults('test@email.com', 1)

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

