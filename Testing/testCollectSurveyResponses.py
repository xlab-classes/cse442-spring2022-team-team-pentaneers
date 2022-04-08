import sys, os, inspect
import datetime
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
parent_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(1, parent_parent_dir)

from Survey.Retrieve.RetrieveSurveyResults import retrieveSurveyResults
from Survey.Create.Response import response
from Survey.Create.Survey import survey
from db_connector import dbConnector
from db_initial import initial,drop
import unittest

class TestStringMethods(unittest.TestCase):

    def test(self):
        drop()

        mydb = dbConnector()
        mycursor = mydb.cursor()

        #get current date,YYYY-MM-DD format
        created_date = datetime.date.today()

        #---------Submitting to a Survey Manually----------------#
        survey_dict = {
            "email": "testingCollectSurvey@email.com",
            "title": "test Collect Survey Responses",
            "description":"test description 1",
            "questions":[['test Collect Survey Responses?', 'Multiple Choice', ['yes', 'no']],
            ['why', 'Short Response', None],
            ['do you want to keep coding?', 'Multiple Choice', ['pain', 'wuyu']]],
            "expired_date": "2022-03-22",
            "visibility":"public"
            }

        retrieved_survey = survey(survey_dict)

        #---------Responding to a Survey Manually----------------#
        response_dict = {
            "email": "testingCollectSurvey@email.com", 
            "survey_id":1,
            "response":[
                ["Multiple Choice", 1],
                ["Short Response","test"],
                ["Multiple Choice", 1]
                ]
            }

        retrieved_response = response(response_dict)

        #--------------Checking for Expected Outcomes-------------------#
        expected_outcome = [[['test Collect Survey Responses?', 'do you want to keep coding?'], [['yes', 'no'], ['pain', 'wuyu']], [[1, 0], [1, 0]]], [['why'], [['testingCollectSurvey@email.com wrote: test']]], 1]


        # Call the function we're testing to see if returned what we wanted
        actual_outcome = retrieveSurveyResults('testingCollectSurvey@email.com', 1)
        print("This is the retrieved outcome: ", actual_outcome)
        self.assertEqual(str(expected_outcome), str(actual_outcome))

        mycursor.close()
        

if __name__ == '__main__':
    unittest.main()