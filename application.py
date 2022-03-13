import datetime
import email
import json
from typing import List
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request
import mysql.connector
from datetime import date
import db_connector, Retrieve
from Delete import Delete

app = Flask(__name__)

# IMPORTANT: Set to environment variable!
app.config['SECRET_KEY']

# Adding in UB's MYSQL Database (Make sure to change the formatting)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mahdyfer:@oceanus.cse.buffalo.edu/cse442_2022_spring_team_ab_db'

# Initialize the database
#Database = SQLAlchemy(app)




app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/submitSurvey", methods=['POST'])
def createSurvey():

    #Assume data are send in json map format
    data=json.loads(request.get_data(as_text=True))
    #print(data)
    email=data['email']
    title=data['title']
    description=data['description']
    questions=data['questions']
    expired=data['expired_date']
    expired=datetime.datetime.strptime(expired,"%Y-%m-%d").date()

    #get current date,YYYY-MM-DD format
    created_date=date.today()

    #var need to be calculated
    countrow = -1
    id = -1
    surveys_id = -1
    question_id = -1 #id in Questions
    relation_id = -1

    # connect database
    mydb = db_connector.dbConnector("root","Ferdaosm50313245!")
    mycursor = mydb.cursor()

    # create table Surveys if not exists
    sql = "CREATE TABLE IF NOT EXISTS Surveys (id int AUTO_INCREMENT PRIMARY KEY, email varchar(255), title varchar(255), description varchar(255), created_on DATE, expired_on Date, surveys_id int)"
    mycursor.execute(sql)
    mydb.commit()

    # create table Survey_Questions if not exists
    sql = "CREATE TABLE IF NOT EXISTS Survey_Questions (id int AUTO_INCREMENT PRIMARY KEY, question_id int, survey_id int)"
    mycursor.execute(sql)
    mydb.commit()

    # create table Questions if not exists
    sql = "CREATE TABLE IF NOT EXISTS Questions (id int AUTO_INCREMENT PRIMARY KEY, survey_id int, question_id int, question_title varchar(255), question_type varchar(255), options varchar(255))"
    mycursor.execute(sql)
    mydb.commit()

    # select surveys_id
    if (countrow == 0):
        surveys_id = 1
    else:
        sqlmax = "select max(surveys_id) from Surveys where email= %s"
        val=(email,)
        mycursor.execute(sqlmax,val)
        surveys = mycursor.fetchall()
        for row in surveys:
            surveys_id = row[0]
        if(surveys_id is None):
            surveys_id=1
        else: surveys_id += 1

    #insert data into Surveys
    sql="Insert into Surveys (email, title, description, created_on, expired_on, surveys_id) values (%s,%s,%s,%s,%s,%s)"
    val=(email,title,description,created_date,expired,surveys_id)
    mycursor.execute(sql,val)
    mydb.commit()

    # for Questions table
    questionnumberList=[]

    #select created id
    sql = "select max(id) from Surveys where email=%s"
    val = (email,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    returnid = 0
    for result in myresult:
        returnid += int(str(result[0]))
    id=returnid

    # insert data into Questions
    for question in questions:
        question_number=question[0] #question_id in Questions
        question_title=question[1]
        question_type=question[2]
        question_id += 1
        questionnumberList.append(question_number)
        if(question[3] is None):
            sql = "Insert into Questions (survey_id, question_id, question_title, question_type) values (%s,%s,%s,%s)"
            val = (id,question_number, question_title, question_type)
            mycursor.execute(sql, val)
            mydb.commit()
        else:
            index=0
            options=""
            for choice in question[3]:
                index+=1
                options+=str(index)+":"+choice+";"
            sql = "Insert into Questions (survey_id, question_id, question_title, question_type, options) values (%s,%s,%s,%s,%s)"
            val = (id,question_number, question_title, question_type, options)
            mycursor.execute(sql, val)
            mydb.commit()

    #insert into Survey_Questions
    for question in questionnumberList:
        relation_id += 1
        sql = "Insert into Survey_Questions ( question_id, survey_id) values (%s,%s)"
        val = (question,id)
        mycursor.execute(sql, val)
        mydb.commit()

    mydb.close()
    return json.dumps(id)

@app.route("/signup", methods=['POST'])
def createAccount():
    data=json.loads(request.get_data(as_text=True))
    email=data['email']
    password=data['password']
    created_date = date.today()

    # connect database
    mydb = db_connector.dbConnector("root","Ferdaosm50313245!")
    mycursor = mydb.cursor()

    #create table if not exists
    sql = "create table if not exists Users (id int AUTO_INCREMENT PRIMARY KEY, email varchar(255), password varchar(255), date_created DATE )"
    mycursor.execute(sql)
    mydb.commit()

    #check account is created or not
    sql = "select * from Users where email=%s"
    val = (email,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    if(len(myresult)!=0): return "account exists"

    #insert user information
    sql = "Insert into Users (email, password, date_created) values (%s,%s,%s)"
    val = (email, password, created_date)
    mycursor.execute(sql, val)
    mydb.commit()

    #select user_id
    sql = "select id from Users where email=%s"
    val = (email,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    returnid=0
    print(myresult)
    for result in myresult:
        returnid+=int(str(result[0]))

    mydb.close()
    return json.dumps(returnid)

@app.route("/submitResponse", methods=['POST'])
def createResponse():

    #get body of the request
    data=json.loads(request.get_data(as_text=True))
    responses=data['response']
    survey_id=data['survey_id']
    email=data['email']

    #connect database
    mydb = db_connector.dbConnector("root","Ferdaosm50313245!")
    mycursor = mydb.cursor()

    sql = "create table if not exists Response (response_id int AUTO_INCREMENT PRIMARY KEY, question_id int, survey_id int,short_answer varchar(255), multiple_choice_answer varchar(255), email varchar(255))"
    mycursor.execute(sql)
    mydb.commit()

    #insert each response
    for response in responses:
        question_number = response[0]  # question_id in Questions
        question_type = response[1]
        answer = response[2]
        if(question_type=="Short Response"):
            sql = "Insert into Response (question_id, survey_id, short_answer, email) values (%s,%s,%s,%s)"
            val = (question_number, survey_id, answer, email)
            mycursor.execute(sql, val)
            mydb.commit()
        else:
            sql = "Insert into Response (question_id, survey_id, multiple_choice_answer, email) values (%s,%s,%s,%s)"
            val = (question_number, survey_id, int(answer),email)
            mycursor.execute(sql, val)
            mydb.commit()

    mydb.close()
    return json.dumps(survey_id)

@app.route("/retrieve/userSurveys/<email>", methods=['GET'])
#User must be logged in, and must also be retreiving their own surveys

# Retrieve all surveys created by the user by their EMAIL
def retrieveSurveysUsers(email):
    retrieve = Retrieve.retrieveSurveysUsers(email)
    return retrieve
    



@app.route("/retrieve/survey/<email>/<survey_id>/results", methods=['GET'])
#User must be logged in, and must also be retreiving data on their own surveys

# Retrieve specific survey results
def retrieveSurveyResults(email, survey_id):

    return "Still need to implement"
   

@app.route('/retrieve/PublicSurveys')
# User does NOT have to be logged in to see public surveys
def retrievePublicSurveys():
    all_surveys = Retrieve.retrievePublicSurveys()
    
    return all_surveys
    





@app.route("/survey/delete/<email>/<id>", methods = ['DELETE'])

def deleteSurvey(email, id):
    deleted_surveys = Delete.deleteSurvey(email, id)
    return deleted_surveys





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
    #app.run(debug = True) # Set to false for production
