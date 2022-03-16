import sys, os, inspect
import datetime
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
parent_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(1, parent_parent_dir)

from Survey.Retrieve.RetrieveUserSurveys import retrieveSurveysUsers
from Survey.Create.Response import response
from Survey.Create.Survey import survey
from db_connector import dbConnector

def test():

    mydb = dbConnector()
    mycursor = mydb.cursor()

    #get current date,YYYY-MM-DD format
    created_date = datetime.date.today()

    #---------Submitting to a Survey Manually----------------#
    survey_dict_1 = {
        "email": "test@email.com",
        "title": "test1",
        "description":"test description 1",
        "questions":[['do you like cats?', 'Multiple Choice', ['yes', 'no']],
        ['why', 'Short Response', None],
        ['do you want to keep coding?', 'Multiple Choice', ['pain', 'wuyu']]],
        "expired_date": "2022-03-22",
        "visibility":"public"
        }

    retrieved_survey = survey(survey_dict_1)
    
    survey_dict_2 = {
        "email": "test@email.com",
        "title": "test2",
        "description":"test description 2",
        "questions":[['do you like cats?', 'Multiple Choice', ['yes', 'no']],
        ['why', 'Short Response', None],
        ['do you want to keep coding?', 'Multiple Choice', ['pain', 'wuyu']]],
        "expired_date": "2022-03-22",
        "visibility":"public"
        }

    retrieved_survey = survey(survey_dict_2)

    expected_outcome = [
        'test@email.com',
        [{'test1': 1}, {'test2': 2}]
    ]

    actual_outcome = retrieveSurveysUsers('test@email.com')

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



