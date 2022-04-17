import datetime
import unittest

import requests

from db_initial import initial,drop
from db_connector import dbConnector
from Survey.Create import Survey
from Survey.Status import Close,Open,Auto

class MyTestCase(unittest.TestCase):

    def test_close_reopen_auto_close_survey(self):
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
        print(survey)
        self.assertEqual(survey[0][0], 'close')







