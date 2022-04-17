
import sys, os, inspect
import datetime
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
parent_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(1, parent_parent_dir)

from db_initial import initial,drop
from db_connector import dbConnector
import unittest
from Survey.Retrieve.RetrieveSurveyForResponse import retrieveSurveyForResponse
from Survey.Create.Response import response

from db_connector import dbConnector
from Survey.Create import Survey
from Survey.Status import Close,Open,Auto
from Survey.Retrieve import RetrievePublicSurveys

class MyTestCase(unittest.TestCase):

    def test_bugs(self):
        drop()
        initial()
        mydb = dbConnector()
        mycursor = mydb.cursor()
        dict1 = {
            "email": "example@buffalo.edu",
            "title": "test1",
            "description": "test survey1",
            "questions": [["test_title1", "Multiple Choice", ["yes", "nonono"]],
                          ["test_title2", "Multiple Choice", ["lipu", "wuyu"]]],
            "expired_date": 1800000000,
            "visibility": "private"
        }
        #submit survey
        sql = "Insert into Surveys (email, title, description, created_on, expired_on, surveys_id,visibility,unique_url,unique_string,status) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = ("example@buffalo.edu", "test1", "test survey1", 1500000000, 1600000000, 1, "private", "asdf", "unique_string", "open")
        mycursor.execute(sql, val)
        mydb.commit()
        answer2 = Close.closeSurvey(1, "example@buffalo.edu")
        mydb = dbConnector()
        mycursor = mydb.cursor()
        #check status
        query = "SELECT status FROM Surveys WHERE id = 1"
        mycursor.execute(query)
        survey = mycursor.fetchall()
        self.assertEqual(survey[0][0], 'close')
        #check expired date
        query = "SELECT expired_on FROM Surveys WHERE id = 1"
        mycursor.execute(query)
        survey = mycursor.fetchall()
        self.assertEqual(survey[0][0], None)
        # reopen survey
        answer2 = Open.openSurvey(1, "example@buffalo.edu")
        mydb = dbConnector()
        mycursor = mydb.cursor()
        # check status
        query = "SELECT status FROM Surveys WHERE id = 1"
        mycursor.execute(query)
        survey = mycursor.fetchall()
        self.assertEqual(survey[0][0], 'open')
        # submit survey
        sql = "Insert into Surveys (email, title, description, created_on, expired_on, surveys_id,visibility,unique_url,unique_string,status) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = ("example@buffalo.edu", "test1", "test survey1", 1400000000, 1500000000, 2, "private", "asdf", "unique_string", "open")
        mycursor.execute(sql, val)
        mydb.commit()
        Auto.autoClose()
        query = "SELECT status FROM Surveys WHERE id = 2"
        mycursor.execute(query)
        survey = mycursor.fetchall()
        self.assertEqual(survey[0][0], 'close')


        
        #submit survey
        sql = "Insert into Surveys (email, title, description, created_on, expired_on, surveys_id,visibility,unique_url,unique_string,status) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = ("example@buffalo.edu", "test2", "test survey2", 1500000000, 1600000000, 3, "private", "asdf", "/test/123", "open")
        mycursor.execute(sql, val)
        mydb.commit()
        sql = "Insert into Questions (id, survey_id, question_id, question_title, question_type, options) values (%s,%s,%s,%s,%s,%s)"
        val = ("3", "3", "3", "question 1", "Multiple Choice", "1;lol;2:lord;")
        mycursor.execute(sql, val)
        mydb.commit()
        sql = "Insert into Response (response_id, question_id, survey_id, short_answer, multiple_choice_answer, email) values (%s,%s,%s,%s,%s,%s)"
        val = ("3", "3", "3", None, 1, "test@email.com")
        mycursor.execute(sql, val)
        mydb.commit()
        data = retrieveSurveyForResponse(3)
        self.assertEqual(data[0], 'example@buffalo.edu')
        self.assertEqual(data[1], 'test2')
        self.assertEqual(data[2], 'test survey2')
        self.assertEqual(data[3], {'question_3': ['question 1', 'Multiple Choice', ['1', 'lol', 'lord']]})


        update_visibilty = "UPDATE Surveys SET status = %s WHERE id = 3"
        val = ("close", )
        mycursor.execute(update_visibilty, val)
        mydb.commit()
        
        
        allSurveys = RetrievePublicSurveys.retrievePublicSurveys()
        self.assertEqual(allSurveys, None)

        update_visibilty = "UPDATE Surveys SET status = %s, visibility = %s WHERE id = 3"
        val = ("open", "public", )
        mycursor.execute(update_visibilty, val)
        mydb.commit()

        allSurveys = RetrievePublicSurveys.retrievePublicSurveys()
        self.assertEqual(allSurveys, "[{'survey_id': 3, 'survey_title': 'test2', 'survey_description': 'test survey2'}]")
        
        return



if __name__ == '__main__':
    unittest.main()