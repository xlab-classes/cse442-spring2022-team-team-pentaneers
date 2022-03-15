import json
import unittest
#from flask import request
import requests
import db_connector
class MyTestCase(unittest.TestCase):
    path='http://172.16.42.82:8899/'
    def test_submitSurvey(self):
        url=self.path+'submitSurvey'

        # initialize database
        mydb = db_connector.dbConnector("root")
        mycursor = mydb.cursor()
        sql = "drop TABLE IF EXISTS Surveys"
        mycursor.execute(sql)
        mydb.commit()
        sql = "drop TABLE IF EXISTS Survey_Questions"
        mycursor.execute(sql)
        mydb.commit()
        sql = "drop TABLE IF EXISTS Questions"
        mycursor.execute(sql)
        mydb.commit()
        mydb.close()

        #insert the first survey with user1
        mydb = db_connector.dbConnector("root")
        mycursor = mydb.cursor()
        dict1={
            "email": "example@buffalo.edu",
            "title": "test1",
            "description": "test survey1",
            "questions": [["test_title1", "Multiple Choice", ["yes", "nonono"]],
                          ["test_title2", "Multiple Choice", ["lipu", "wuyu"]]],
            "expired_date": "2022-03-16",
            "visibility": "private"
        }
        r = requests.post(url,json=dict1)
        answer1=r.json()
        self.assertEqual(answer1, 1)  # add assertion here

        #check number of rows for each tables
        sql = "select * from surveys;"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        self.assertEqual(len(myresult), 1)
        sql = "select * from questions;"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        self.assertEqual(len(myresult), 2)
        sql = "select * from survey_questions;"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        self.assertEqual(len(myresult), 2)

        # check content with specific id
        sql = "select * from Surveys where id=%s;"
        val = (answer1,)
        mycursor.execute(sql,val)
        myresult=mycursor.fetchall()
        result=list(myresult[0])
        self.assertEqual(result[1], dict1["email"])
        self.assertEqual(result[2], dict1["title"])
        self.assertEqual(result[3], dict1["description"])
        self.assertEqual(result[6], 1)
        self.assertEqual(result[7], dict1["visibility"])
        sql = "select * from Questions where survey_id=%s;"
        val = (answer1,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        result1 = list(myresult[0])
        result2 = list(myresult[1])
        self.assertEqual(result1[0], 1)
        self.assertEqual(result1[1], answer1)
        self.assertEqual(result1[2], 1)
        self.assertEqual(result1[3], dict1["questions"][0][0])
        self.assertEqual(result1[4], dict1["questions"][0][1])
        self.assertEqual(result1[5], "1:yes;2:nonono;")
        self.assertEqual(result2[0], 2)
        self.assertEqual(result2[1], answer1)
        self.assertEqual(result2[2], 2)
        self.assertEqual(result2[3], dict1["questions"][1][0])
        self.assertEqual(result2[4], dict1["questions"][1][1])
        self.assertEqual(result2[5], "1:lipu;2:wuyu;")
        sql = "select * from Survey_Questions where survey_id=%s;"
        val = (answer1,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        result1 = list(myresult[0])
        result2 = list(myresult[1])
        self.assertEqual(result1[0], 1)
        self.assertEqual(result1[1], 1)
        self.assertEqual(result1[2], answer1)
        self.assertEqual(result2[0], 2)
        self.assertEqual(result2[1], 2)
        self.assertEqual(result2[2], answer1)
        mydb.close()

        # insert the second survey with user1
        mydb = db_connector.dbConnector("root")
        mycursor = mydb.cursor()
        dict2 = {
            "email": "example@buffalo.edu",
            "title": "test2",
            "description": "test survey2",
            "questions": [["test_title1", "Multiple Choice", ["yes", "nonono"]],
                          ["test_title2", "Multiple Choice", ["lipu", "wuyu"]]],
            "expired_date": "2022-03-16",
            "visibility": "private"
        }
        r = requests.post(url, json=dict2)
        answer2 = r.json()

        # check number of rows for each table
        self.assertEqual(answer2, 2)
        sql = "select * from surveys;"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        self.assertEqual(len(myresult), 2)
        sql = "select * from questions;"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        self.assertEqual(len(myresult), 4)
        sql = "select * from survey_questions;"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        self.assertEqual(len(myresult), 4)

        #check content with specific id
        sql = "select * from Surveys where id=%s;"
        val = (answer2,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        result = list(myresult[0])
        self.assertEqual(result[1], dict2["email"])
        self.assertEqual(result[2], dict2["title"])
        self.assertEqual(result[3], dict2["description"])
        self.assertEqual(result[6], 2)
        self.assertEqual(result[7], dict2["visibility"])
        sql = "select * from Questions where survey_id=%s;"
        val = (answer2,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        result1 = list(myresult[0])
        result2 = list(myresult[1])
        self.assertEqual(result1[0], 3)
        self.assertEqual(result1[1], answer2)
        self.assertEqual(result1[2], 1)
        self.assertEqual(result1[3], dict1["questions"][0][0])
        self.assertEqual(result1[4], dict1["questions"][0][1])
        self.assertEqual(result1[5], "1:yes;2:nonono;")
        self.assertEqual(result2[0], 4)
        self.assertEqual(result2[1], answer2)
        self.assertEqual(result2[2], 2)
        self.assertEqual(result2[3], dict1["questions"][1][0])
        self.assertEqual(result2[4], dict1["questions"][1][1])
        self.assertEqual(result2[5], "1:lipu;2:wuyu;")
        sql = "select * from Survey_Questions where survey_id=%s;"
        val = (answer2,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        result1 = list(myresult[0])
        result2 = list(myresult[1])
        self.assertEqual(result1[0], 3)
        self.assertEqual(result1[1], 1)
        self.assertEqual(result1[2], answer2)
        self.assertEqual(result2[0], 4)
        self.assertEqual(result2[1], 2)
        self.assertEqual(result2[2], answer2)
        mydb.close()

        # insert the first survey with user2
        mydb = db_connector.dbConnector("root")
        mycursor = mydb.cursor()
        dict3 = {
            "email": "example2@buffalo.edu",
            "title": "test1",
            "description": "test survey1",
            "questions": [["test_title1", "Multiple Choice", ["yes", "nonono"]],
                          ["test_title2", "Multiple Choice", ["lipu", "wuyu"]]],
            "expired_date": "2022-03-16",
            "visibility": "private"
        }
        # dict1=json.dumps(dict1)
        # print(type(dict1))
        r = requests.post(url, json=dict3)
        answer3 = r.json()
        self.assertEqual(answer3, 3)

        # check number of rows for each table
        sql = "select * from surveys;"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        self.assertEqual(len(myresult), 3)
        sql = "select * from questions;"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        self.assertEqual(len(myresult), 6)
        sql = "select * from survey_questions;"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        self.assertEqual(len(myresult), 6)

        # check content with specific id
        sql = "select * from Surveys where id=%s"
        val = (answer3,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        result = list(myresult[0])
        self.assertEqual(result[1], dict3["email"])
        self.assertEqual(result[2], dict3["title"])
        self.assertEqual(result[3], dict3["description"])
        self.assertEqual(result[6], 1)
        self.assertEqual(result[7], dict3["visibility"])
        sql = "select * from Questions where survey_id=%s;"
        val = (answer3,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        result1 = list(myresult[0])
        result2 = list(myresult[1])
        self.assertEqual(result1[0], 5)
        self.assertEqual(result1[1], answer3)
        self.assertEqual(result1[2], 1)
        self.assertEqual(result1[3], dict1["questions"][0][0])
        self.assertEqual(result1[4], dict1["questions"][0][1])
        self.assertEqual(result1[5], "1:yes;2:nonono;")
        self.assertEqual(result2[0], 6)
        self.assertEqual(result2[1], answer3)
        self.assertEqual(result2[2], 2)
        self.assertEqual(result2[3], dict1["questions"][1][0])
        self.assertEqual(result2[4], dict1["questions"][1][1])
        self.assertEqual(result2[5], "1:lipu;2:wuyu;")
        sql = "select * from Survey_Questions where survey_id=%s;"
        val = (answer3,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        result1 = list(myresult[0])
        result2 = list(myresult[1])
        self.assertEqual(result1[0], 5)
        self.assertEqual(result1[1], 1)
        self.assertEqual(result1[2], answer3)
        self.assertEqual(result2[0], 6)
        self.assertEqual(result2[1], 2)
        self.assertEqual(result2[2], answer3)
        mydb.close()

        # insert the second survey with user2
        mydb = db_connector.dbConnector("root")
        mycursor = mydb.cursor()
        dict4 = {
            "email": "example2@buffalo.edu",
            "title": "test2",
            "description": "test survey2",
            "questions": [["test_title1", "Multiple Choice", ["yes", "nonono"]],
                          ["test_title2", "Multiple Choice", ["lipu", "wuyu"]]],
            "expired_date": "2022-03-16",
            "visibility": "private"
        }
        # dict1=json.dumps(dict1)
        # print(type(dict1))
        r = requests.post(url, json=dict4)
        answer4 = r.json()
        self.assertEqual(answer4, 4)

        # check number of rows for each table
        sql = "select * from surveys;"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        self.assertEqual(len(myresult), 4)
        sql = "select * from questions;"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        self.assertEqual(len(myresult), 8)
        sql = "select * from survey_questions;"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        self.assertEqual(len(myresult), 8)

        # check content with specific id
        sql = "select * from Surveys where id=%s"
        val = (answer4,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        result = list(myresult[0])
        self.assertEqual(result[1], dict4["email"])
        self.assertEqual(result[2], dict4["title"])
        self.assertEqual(result[3], dict4["description"])
        self.assertEqual(result[6], 2)
        self.assertEqual(result[7], dict4["visibility"])
        sql = "select * from Questions where survey_id=%s;"
        val = (answer4,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        result1 = list(myresult[0])
        result2 = list(myresult[1])
        self.assertEqual(result1[0], 7)
        self.assertEqual(result1[1], answer4)
        self.assertEqual(result1[2], 1)
        self.assertEqual(result1[3], dict1["questions"][0][0])
        self.assertEqual(result1[4], dict1["questions"][0][1])
        self.assertEqual(result1[5], "1:yes;2:nonono;")
        self.assertEqual(result2[0], 8)
        self.assertEqual(result2[1], answer4)
        self.assertEqual(result2[2], 2)
        self.assertEqual(result2[3], dict1["questions"][1][0])
        self.assertEqual(result2[4], dict1["questions"][1][1])
        self.assertEqual(result2[5], "1:lipu;2:wuyu;")
        sql = "select * from Survey_Questions where survey_id=%s;"
        val = (answer4,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        result1 = list(myresult[0])
        result2 = list(myresult[1])
        self.assertEqual(result1[0], 7)
        self.assertEqual(result1[1], 1)
        self.assertEqual(result1[2], answer4)
        self.assertEqual(result2[0], 8)
        self.assertEqual(result2[1], 2)
        self.assertEqual(result2[2], answer4)
        mydb.close()

        # insert the third survey with user1
        mydb = db_connector.dbConnector("root")
        mycursor = mydb.cursor()
        dict5 = {
            "email": "example@buffalo.edu",
            "title": "test3",
            "description": "test survey3",
            "questions": [["test_title1", "Multiple Choice", ["yes", "nonono"]],
                          ["test_title2", "Multiple Choice", ["lipu", "wuyu"]]],
            "expired_date": "2022-03-16",
            "visibility": "private"
        }
        # dict1=json.dumps(dict1)
        # print(type(dict1))
        r = requests.post(url, json=dict5)
        answer5 = r.json()
        self.assertEqual(answer5, 5)

        # check number of rows for each table
        sql = "select * from surveys;"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        self.assertEqual(len(myresult), 5)
        sql = "select * from questions;"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        self.assertEqual(len(myresult), 10)
        sql = "select * from survey_questions;"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        self.assertEqual(len(myresult), 10)

        # check content with specific id
        sql = "select * from Surveys where id=%s"
        val = (answer5,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        result = list(myresult[0])
        self.assertEqual(result[1], dict5["email"])
        self.assertEqual(result[2], dict5["title"])
        self.assertEqual(result[3], dict5["description"])
        self.assertEqual(result[6], 3)
        self.assertEqual(result[7], dict5["visibility"])
        sql = "select * from Questions where survey_id=%s;"
        val = (answer5,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        result1 = list(myresult[0])
        result2 = list(myresult[1])
        self.assertEqual(result1[0], 9)
        self.assertEqual(result1[1], answer5)
        self.assertEqual(result1[2], 1)
        self.assertEqual(result1[3], dict1["questions"][0][0])
        self.assertEqual(result1[4], dict1["questions"][0][1])
        self.assertEqual(result1[5], "1:yes;2:nonono;")
        self.assertEqual(result2[0], 10)
        self.assertEqual(result2[1], answer5)
        self.assertEqual(result2[2], 2)
        self.assertEqual(result2[3], dict1["questions"][1][0])
        self.assertEqual(result2[4], dict1["questions"][1][1])
        self.assertEqual(result2[5], "1:lipu;2:wuyu;")
        sql = "select * from Survey_Questions where survey_id=%s;"
        val = (answer5,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        result1 = list(myresult[0])
        result2 = list(myresult[1])
        self.assertEqual(result1[0], 9)
        self.assertEqual(result1[1], 1)
        self.assertEqual(result1[2], answer5)
        self.assertEqual(result2[0], 10)
        self.assertEqual(result2[1], 2)
        self.assertEqual(result2[2], answer5)
        mydb.close()

    def test_signup(self):
        url=self.path+'signup'
        mydb = db_connector.dbConnector("root")
        mycursor = mydb.cursor()
        sql = "drop TABLE IF EXISTS Users"
        mycursor.execute(sql)
        mydb.commit()
        mydb.close()

        # create user1
        mydb = db_connector.dbConnector("root")
        mycursor = mydb.cursor()
        dict1 = {
           "email": "example@buffalo.edu",
           "password":"a2"
        }
        r = requests.post(url, json=dict1)
        answer1 = r.json()
        self.assertEqual(answer1, 1)  # add assertion here

        # check content with specific id
        sql = "select * from Users where id=%s;"
        val = (answer1,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        result = list(myresult[0])
        self.assertEqual(result[1], dict1["email"])
        self.assertEqual(result[2], dict1["password"])
        mydb.close()

        # insert the second survey with user1
        mydb = db_connector.dbConnector("root")
        mycursor = mydb.cursor()
        dict2 = {
            "email": "example2@buffalo.edu",
            "password": "a2"
        }
        r = requests.post(url, json=dict2)
        answer2 = r.json()
        self.assertEqual(answer2, 2)

        # check content with specific id
        sql = "select * from Users where id=%s;"
        val = (answer2,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        result = list(myresult[0])
        self.assertEqual(result[1], dict2["email"])
        self.assertEqual(result[2], dict2["password"])
        mydb.close()

        # try to create account which is created
        mydb = db_connector.dbConnector("root")
        mycursor = mydb.cursor()
        dict3 = {
            "email": "example2@buffalo.edu",
            "password": "a4"
        }
        r = requests.post(url, json=dict3)
        answer3 = r.json()
        self.assertEqual(answer3,"account exists")
        mydb.close()

    def test_response(self):
        url = self.path + 'submitResponse'
        mydb = db_connector.dbConnector("root")
        mycursor = mydb.cursor()
        sql = "drop TABLE IF EXISTS Response"
        mycursor.execute(sql)
        mydb.commit()
        mydb.close()

        # create user1
        mydb = db_connector.dbConnector("root")
        mycursor = mydb.cursor()
        dict1 = {
           "email": "example@buffalo.edu",
           "survey_id":1,
           "response":[["Short Response","haha"],["Multiple Choice", 1],["Multiple Choice", 1]]
        }

        r = requests.post(url, json=dict1)
        answer1 = r.json()
        # print(answer1)
        self.assertEqual(answer1, 1)  # add assertion here

        # check content with specific id
        sql = "select * from Response where survey_id=%s;"
        val = (answer1,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        result1 = list(myresult[0])
        result2 = list(myresult[1])
        result3 = list(myresult[2])
        self.assertEqual(result1[0], 1)
        self.assertEqual(result1[1], 1)
        self.assertEqual(result1[2], answer1)
        self.assertEqual(result1[3], "haha")
        self.assertEqual(result1[4], None)
        self.assertEqual(result1[5], dict1["email"])
        self.assertEqual(result2[0], 2)
        self.assertEqual(result2[1], 2)
        self.assertEqual(result2[2], answer1)
        self.assertEqual(result2[3], None)
        self.assertEqual(result2[4], "1")
        self.assertEqual(result2[5], dict1["email"])
        self.assertEqual(result3[0], 3)
        self.assertEqual(result3[1], 3)
        self.assertEqual(result3[2], answer1)
        self.assertEqual(result3[3], None)
        self.assertEqual(result3[4], "1")
        self.assertEqual(result3[5], dict1["email"])
        mydb.close()

        # insert the second survey with user1
        mydb = db_connector.dbConnector("root")
        mycursor = mydb.cursor()
        dict2 = {
           "email": "example2@buffalo.edu",
           "survey_id":4,
           "response":[["Multiple Choice", 1],["Short Response","wuyu"],["Multiple Choice", 1]]
        }
        r = requests.post(url, json=dict2)
        answer2 = r.json()
        self.assertEqual(answer2, dict2["survey_id"])

        # check content with specific id
        sql = "select * from Response where survey_id=%s;"
        val = (answer2,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        result1 = list(myresult[0])
        result2 = list(myresult[1])
        result3 = list(myresult[2])
        self.assertEqual(result1[0], 4)
        self.assertEqual(result1[1], 1)
        self.assertEqual(result1[2], answer2)
        self.assertEqual(result1[3], None)
        self.assertEqual(result1[4], "1")
        self.assertEqual(result1[5], dict2["email"])
        self.assertEqual(result2[0], 5)
        self.assertEqual(result2[1], 2)
        self.assertEqual(result2[2], answer2)
        self.assertEqual(result2[3], "wuyu")
        self.assertEqual(result2[4], None)
        self.assertEqual(result2[5], dict2["email"])
        self.assertEqual(result3[0], 6)
        self.assertEqual(result3[1], 3)
        self.assertEqual(result3[2], answer2)
        self.assertEqual(result3[3], None)
        self.assertEqual(result3[4], "1")
        self.assertEqual(result3[5], dict2["email"])
        mydb.close()

        # try to create account which is created
        mydb = db_connector.dbConnector("root")
        mycursor = mydb.cursor()
        dict3 = {
           "email": "example2@buffalo.edu",
           "survey_id":4,
           "response":[["Multiple Choice", 1],["Short Response","lipu"],["Multiple Choice", 1]]
        }
        r = requests.post(url, json=dict3)
        answer3 = r.json()
        self.assertEqual(answer3, dict3["survey_id"])

        # it should have all responses of specific id
        sql = "select * from Response where survey_id=%s;"
        val = (answer3,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        result1 = list(myresult[0])
        result2 = list(myresult[1])
        result3 = list(myresult[2])
        result4 = list(myresult[3])
        result5 = list(myresult[4])
        result6 = list(myresult[5])
        self.assertEqual(result1[0], 4)
        self.assertEqual(result1[1], 1)
        self.assertEqual(result1[2], answer3)
        self.assertEqual(result1[3], None)
        self.assertEqual(result1[4], "1")
        self.assertEqual(result1[5], dict2["email"])
        self.assertEqual(result2[0], 5)
        self.assertEqual(result2[1], 2)
        self.assertEqual(result2[2], answer3)
        self.assertEqual(result2[3], "wuyu")
        self.assertEqual(result2[4], None)
        self.assertEqual(result2[5], dict2["email"])
        self.assertEqual(result3[0], 6)
        self.assertEqual(result3[1], 3)
        self.assertEqual(result3[2], answer3)
        self.assertEqual(result3[3], None)
        self.assertEqual(result3[4], "1")
        self.assertEqual(result3[5], dict2["email"])
        self.assertEqual(result4[0], 7)
        self.assertEqual(result4[1], 1)
        self.assertEqual(result4[2], answer3)
        self.assertEqual(result4[3], None)
        self.assertEqual(result4[4], "1")
        self.assertEqual(result4[5], dict2["email"])
        self.assertEqual(result5[0], 8)
        self.assertEqual(result5[1], 2)
        self.assertEqual(result5[2], answer3)
        self.assertEqual(result5[3], "lipu")
        self.assertEqual(result5[4], None)
        self.assertEqual(result5[5], dict2["email"])
        self.assertEqual(result6[0], 9)
        self.assertEqual(result6[1], 3)
        self.assertEqual(result6[2], answer3)
        self.assertEqual(result6[3], None)
        self.assertEqual(result6[4], "1")
        self.assertEqual(result6[5], dict2["email"])
        mydb.close()



if __name__ == '__main__':
    unittest.main()
