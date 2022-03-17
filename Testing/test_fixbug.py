import unittest

import requests

from db_initial import initial,drop
from db_connector import dbConnector

class MyTestCase(unittest.TestCase):
    path = 'http://172.16.42.82:8000/'

    def testModifySurvey(self):
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
            "expired_date": "2022-03-16",
            "visibility": "private"
        }
        r = requests.post(url, json=dict1)
        answer1 = r.json()
        self.assertEqual(answer1, 1)
        url=self.path+'survey/delete/example@buffalo.edu/1'

        #delete survey
        r = requests.delete(url)
        self.assertEqual(r.content.decode(), "Survey has been deleted for email: example@buffalo.edu with survey_id = 1")

        #try modify
        modi1 = {
            "email": "example@buffalo.edu",
            "title": "test1",
            "description": "test survey1",
            "questions": [["test_title1", "Multiple Choice", ["yes", "nonono"]],
                          ["test_title2", "Multiple Choice", ["lipu", "wuyu"]]],
            "expired_date": "2022-03-16",
            "visibility": "private"
        }
        url = self.path + '/survey/modify/1'
        r = requests.put(url,json=modi1)
        self.assertEqual(r.content.decode(), "survey not exists")
        modi2 = {
            "email": "example@buffalo.edu",
            "title": "test1",
            "description": "test survey1",
            "questions": [["test_title2", "Multiple Choice", ["yes", "nonono"]],
                          ["test_title2", "Multiple Choice", ["lipu", "wuyu"]]],
            "expired_date": "2022-03-16",
            "visibility": "private"
        }
        url = self.path + '/survey/modify/1'
        r = requests.put(url, json=modi2)
        self.assertEqual(r.content.decode(), "survey not exists")
        modi3 = {
            "email": "example@buffalo.edu",
            "title": "test1",
            "description": "test survey1",
            "questions": [["test_title2", "Multiple Choice", ["yes", "nonono"]],
                          ["test_title2", "Multiple Choice", ["lipu", "wuyu"]],
                          ["test_title3", "Multiple Choice", ["wozhendehuixie", "tule","fansi"]]],
            "expired_date": "2022-03-20",
            "visibility": "private"
        }
        url = self.path + '/survey/modify/1'
        r = requests.put(url, json=modi3)
        self.assertEqual(r.content.decode(), "survey not exists")
        mydb.close()

    def testDeleteSurvey(self):
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
                "expired_date": "2022-03-16",
                "visibility": "private"
            }
            r = requests.post(url, json=dict1)
            answer1 = r.json()
            self.assertEqual(answer1, 1)
            url = self.path + 'survey/delete/example@buffalo.edu/1'

            #delete survey
            r = requests.delete(url)
            self.assertEqual(r.content.decode(),
                             "Survey has been deleted for email: example@buffalo.edu with survey_id = 1")

            #try delete
            url = self.path + 'survey/delete/example@buffalo.edu/1'
            r = requests.delete(url)
            self.assertEqual(r.content.decode(), "survey not exists")

            # try delete
            url = self.path + 'survey/delete/example@buffalo.edu/1'
            r = requests.delete(url)
            self.assertEqual(r.content.decode(), "survey not exists")

            # try delete
            url = self.path + 'survey/delete/example@buffalo.edu/1'
            r = requests.delete(url)
            self.assertEqual(r.content.decode(), "survey not exists")
            mydb.close()

    def testRetrieveResults(self):
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
            "expired_date": "2022-03-16",
            "visibility": "private"
        }
        r = requests.post(url, json=dict1)
        answer1 = r.json()
        self.assertEqual(answer1, 1)
        url = self.path + 'survey/delete/example@buffalo.edu/1'

        # delete survey
        r = requests.delete(url)
        self.assertEqual(r.content.decode(),
                         "Survey has been deleted for email: example@buffalo.edu with survey_id = 1")

        # try delete
        url = self.path + 'survey/delete/example@buffalo.edu/1'
        r = requests.delete(url)
        self.assertEqual(r.content.decode(), "survey not exists")

        # try delete
        url = self.path + '/retrieve/survey/example@buffalo.edu/1/results'
        r = requests.get(url)
        self.assertEqual(r.content.decode(), "survey not exists")

        # try delete
        url = self.path + '/retrieve/survey/example@buffalo.edu/1/results'
        r = requests.get(url)
        self.assertEqual(r.content.decode(), "survey not exists")
        mydb.close()





if __name__ == '__main__':
    unittest.main()
