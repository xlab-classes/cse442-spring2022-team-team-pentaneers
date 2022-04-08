import datetime
import unittest

import requests

from db_initial import initial,drop
from db_connector import dbConnector

class MyTestCase(unittest.TestCase):
    path = 'http://172.16.42.82:8000/'

    def testCloseReopenSurvey(self):
        drop()
        initial()
        url = self.path + 'submitSurvey'
        mydb = dbConnector()
        mycursor = mydb.cursor()
        dict1 = {
            "email": "example@buffalo.edu",
            "title": "test1",
            "description": "test survey1",
            "questions": [["test_title1", "Multiple Choice", ["yes", "nonono"]],
                          ["test_title2", "Multiple Choice", ["lipu", "wuyu"]]],
            "expired_date": "2023-04-02",
            "visibility": "public"
        }
        #submit survey
        r = requests.post(url, json=dict1)
        answer1 = r.json()
        self.assertEqual(answer1, 1)
        url = self.path + 'survey/close/1'
        r=requests.put(url)
        mydb = dbConnector()
        mycursor = mydb.cursor()
        #check status
        query = "SELECT visibility FROM Surveys WHERE surveys_id = 1 and email='example@buffalo.edu'"
        mycursor.execute(query)
        survey = mycursor.fetchall()
        self.assertEqual(survey[0][0], 'close')
        #check expired date
        query = "SELECT expired_on FROM Surveys WHERE id = 1"
        mycursor.execute(query)
        survey = mycursor.fetchall()
        self.assertEqual(survey[0][0], None)
        # reopen survey
        url=self.path+'survey/reopen/1'
        dict2={
            "expired_date": "2023-04-02"
        }
        r=requests.put(url,json=dict2)
        mydb = dbConnector()
        mycursor = mydb.cursor()
        # check status
        query = "SELECT visibility FROM Surveys WHERE id = 1"
        mycursor.execute(query)
        survey = mycursor.fetchall()
        self.assertEqual(survey[0][0], 'public')
        # check expired date
        query = "SELECT expired_on FROM Surveys WHERE id = 1"
        mycursor.execute(query)
        survey = mycursor.fetchall()
        expired=datetime.datetime.strptime("2023-04-02", "%Y-%m-%d").date()
        self.assertEqual(survey[0][0], expired)
        url = self.path + 'survey/private/1'
        r = requests.put(url)
        mydb = dbConnector()
        mycursor = mydb.cursor()
        # check status
        query = "SELECT visibility FROM Surveys WHERE surveys_id = 1 and email='example@buffalo.edu'"
        mycursor.execute(query)
        survey = mycursor.fetchall()
        self.assertEqual(survey[0][0], 'private')

    def autoClose(self):
        drop()
        initial()
        url = self.path + 'submitSurvey'
        mydb = dbConnector()
        mycursor = mydb.cursor()
        dict1 = {
            "email": "example@buffalo.edu",
            "title": "test1",
            "description": "test survey1",
            "questions": [["test_title1", "Multiple Choice", ["yes", "nonono"]],
                          ["test_title2", "Multiple Choice", ["lipu", "wuyu"]]],
            "expired_date": "2022-04-02",
            "visibility": "private"
        }
        # submit survey
        r = requests.post(url, json=dict1)
        answer1 = r.json()
        self.assertEqual(answer1, 1)
        url = self.path + 'retrieve/PublicSurveys'
        r = requests.get(url)
        self.assertEqual(len(r), 0)







