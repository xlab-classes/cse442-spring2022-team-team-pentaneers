import datetime
import json
import os,sys,inspect

# All of this code is to just get modules from outside of the 'Testing' directory
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
parent_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(1, parent_parent_dir)


from Retrieve.RetrieveSurveyById import retrieveSurveyById
from create.Response import response
from create.Survey import survey
from db_connector import dbConnector




def test():
    mydb = dbConnector("root")
    mycursor = mydb.cursor()

    survey_id = 1
    email = "test@email.com"

    survey_dict = {
        "email": "test@email.com",
        "title": "test1",
        "description":"test description 1",
        "questions":[['do you like cats?', 'Multiple Choice', ['yes', 'no']],
        ['why', 'Short Response', None],
        ['do you wanna keep coding?', 'Multiple Choice', ['pain', 'wuyu']]],
        "expired_date": "2022-03-22",
        "visibility":"public"
        }

    
    retrieved_survey = survey(survey_dict)

    #get current date,YYYY-MM-DD format
    created_date = datetime.date.today()


    response_dict = {
        "email": "test@email.com", 
        "survey_id":1,
        "response":[["Short Response","test"],["Multiple Choice", 1],["Multiple Choice", 1]]
        }

    
    retrieved_response = response(response_dict)
    

    expected_outcome = [1, 'test@email.com', 'test1', 'test description 1', datetime.date(2022, 3, 22), 
                        {'question_1': ['do you like cats?', 'Multiple Choice', ['yes', 'no']]}, 
                        {'question_2': ['why', 'Short Response', None]},
                        {'question_3': ['do you wanna keep coding?', 'Multiple Choice', ['pain', 'wuyu']]}
                    ]


    actual_outcome = retrieveSurveyById(survey_id, email)
    

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


