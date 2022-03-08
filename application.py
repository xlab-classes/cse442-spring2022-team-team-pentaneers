import datetime
import json
from typing import List
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request
import mysql.connector
from datetime import date

app = Flask(__name__)

# IMPORTANT: Set to environment variable!
app.config['SECRET_KEY']

# Adding in UB's MYSQL Database (Make sure to change the formatting)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mahdyfer:50313245@oceanus.cse.buffalo.edu/cse442_2022_spring_team_ab_db'

# Initialize the database
#Database = SQLAlchemy(app)




@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/submitSurvey", methods=['POST'])
def createSurvey():
    Database = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ferdaosm50313245!",
        database="test_db"
    )
    
    #Assume data are send in json map format
    data=json.loads(request.get_data(as_text=True))
    print(data)
    email=data['email']
    title=data['title']
    description=data['description']
    questions=data['questions']
    expired=data['expired_date']
    expired=datetime.datetime.strptime(expired,"%Y-%m-%d").date()
    print("type"+str(type(expired))+str(expired))
    #get current date,YYYY-MM-DD format
    created_date=date.today()
    #var need to be calculated
    countrow = -1
    id = -1
    surveys_id = -1
    question_id = -1 #id in Questions
    relation_id = -1
    mydb = Database
    mycursor = mydb.cursor()
    #sql = "drop TABLE IF EXISTS Surveys"
    #mycursor.execute(sql)
    #mydb.commit()
    sql = "CREATE TABLE IF NOT EXISTS Surveys (id int, email varchar(255), title varchar(255), description varchar(255), created_on DATE, expired_on DATE, surveys_id int)"
    mycursor.execute(sql)
    mydb.commit()
    #sql = "drop TABLE IF EXISTS Survey_Questions"
    #mycursor.execute(sql)
    #mydb.commit()
    sql = "CREATE TABLE IF NOT EXISTS Survey_Questions (id int, question_id int, survey_id int)"
    mycursor.execute(sql)
    mydb.commit()
    #sql = "drop TABLE IF EXISTS Questions"
    #mycursor.execute(sql)
    #mydb.commit()
    sql = "CREATE TABLE IF NOT EXISTS Questions (id int, question_id int, question_title varchar(255), question_type varchar(255), options varchar(255))"
    mycursor.execute(sql)
    mydb.commit()
    #count if any content in Surveys
    sqlcountSurvey="select count(*) from Surveys"
    mycursor.execute(sqlcountSurvey)
    countresult = mycursor.fetchall()

    for row in countresult:
        countrow = row[0]
    # select id
    if(countrow==0):
        id=1
    else:
        sqlId="select max(id) from Surveys"
        mycursor.execute(sqlId)
        maxId = mycursor.fetchall()
        for row in maxId:
            id = row[0]
        id+=1

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
    sql="Insert into Surveys (id, email, title, description, created_on, expired_on, surveys_id) values (%s,%s,%s,%s,%s,%s,%s)"
    val=(id,email,title,description,created_date,expired,surveys_id)
    mycursor.execute(sql,val)
    mydb.commit()


    questionnumberList=[]
    sqlcountSurvey = "select count(*) from Questions"
    mycursor.execute(sqlcountSurvey)
    countresult = mycursor.fetchall()

    for row in countresult:
        countrow = row[0]
    # select id
    if (countrow == 0):
        question_id = 0
    else:
        sqlmax = "select max(id) from Questions"
        mycursor.execute(sqlmax)
        question_ids = mycursor.fetchall()
        for row in question_ids:
            question_id = row[0]


    # insert data into Questions
    for question in questions:
        question_number=question[0]#question_id in Questions
        question_title=question[1]
        question_type=question[2]
        question_id += 1
        questionnumberList.append(question_number)
        if(question[3] is None):
            sql = "Insert into Questions (id, question_id, question_title, question_type) values (%s,%s,%s,%s)"
            val = (question_id, question_number, question_title, question_type)
            mycursor.execute(sql, val)
            mydb.commit()
            #questionidList.append(question_id)
        else:
            index=0
            options=""
            for choice in question[3]:
                index+=1
                options+=str(index)+":"+choice+";"
            sql = "Insert into Questions (id, question_id, question_title, question_type, options) values (%s,%s,%s,%s,%s)"
            val = (question_id, question_number, question_title, question_type, options)
            mycursor.execute(sql, val)
            mydb.commit()
            #questionidList.append(question_id)

    #insert into Survey_Questions
    sqlcountSurvey = "select count(*) from Survey_Questions"
    mycursor.execute(sqlcountSurvey)
    countresult = mycursor.fetchall()

    for row in countresult:
        countrow = row[0]
    # select id
    if (countrow == 0):
        relation_id = 0
    else:
        sqlmax = "select max(id) from Survey_Questions"
        mycursor.execute(sqlmax)
        relations = mycursor.fetchall()
        for row in relations:
            relation_id = row[0]
    #print(questionnumberList)
    for question in questionnumberList:
        relation_id += 1
        sql = "Insert into Survey_Questions (id, question_id, survey_id) values (%s,%s,%s)"
        val = (relation_id,question,id)
        mycursor.execute(sql, val)
        mydb.commit()
    
    mydb.close()

    return str(id)
    #pass

@app.route("/signup", methods=['POST'])
def createAccount():
    #region...
    data=json.loads(request.get_data(as_text=True))
    email=data['email']
    password=data['password']
    created_date = date.today()
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="50310786",
        database="testdb"
    )
    mycursor = mydb.cursor()
    #sql = "drop table if exists Users"
    #mycursor.execute(sql)
    #mydb.commit()

    #create table if not exists
    sql = "create table if not exists Users (id int AUTO_INCREMENT PRIMARY KEY, email varchar(255), password varchar(255), date_created DATE )"
    mycursor.execute(sql)
    mydb.commit()

    #check account is created or not
    sql = "select * from Users where email=%s"
    val = (email,)
    mycursor.execute(sql, val)
    # mydb.commit()
    myresult = mycursor.fetchall()
    #print(myresult)
    #print(len(myresult))
    if(len(myresult)!=0): return "account exists"

    #insert user information
    sql = "Insert into Users (email, password, date_created) values (%s,%s,%s)"
    val = (email, password, created_date)
    mycursor.execute(sql, val)
    mydb.commit()

    #sql = "select id from Users where email=%s"
    #val = (email,)
    #mycursor.execute(sql,val)
    # mydb.commit()
    sql = "select * from Users"
    #val = (email,)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    returnid=""
    for x in myresult:
        returnid += str(x)
    mydb.close()
    return returnid
    #pass
    #endregion



@app.route("/submitResponse", methods=['POST'])
def createResponse():
    Database = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ferdaosm50313245!",
        database="test_db"
    )
    #get body of the request
    data=json.loads(request.get_data(as_text=True))
    responses=data['response']
    survey_id=data['survey_id']
    email=data['email']
    mydb = Database
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
    sql = "select * from Response"
    # val = (email,)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    returnid = ""
    for x in myresult:
        returnid += str(x)
    mydb.close()
    return returnid


@app.route("/retrieve/userSurveys/<email>", methods=['GET'])
#User must be logged in, and must also be retreiving their own surveys

# Retrieve all surveys created by the user by their EMAIL
def retrieveSurveysUsers(email):
    List_to_return = []
    Database = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ferdaosm50313245!",
        database="test_db"
    )
    # Access the Database
    mydb = Database
    mycursor = mydb.cursor()
    # Select only the rows that have our requested "email" 
    query = "SELECT * FROM Surveys WHERE email = %s"
    user_email = (email, )

    # Execute our MySQL Query to get what we want
    mycursor.execute(query, user_email)
    # fetch all the matching rows 
    result = mycursor.fetchall()
    
    # loop through the rows that have only the requested email in them and 
    # row format = [id, email, title, description, created_on, expire, surveys_id]
    for row in result:
        dictionary = {}
        # Get the surveys_id, this will act as a Value
        surveys_id = row[6]
        # Get the survey_title, this will act as a Key
        survey_title = row[2]
        dictionary[survey_title] = surveys_id
        # Append the created dictionary to the list that we are going to return
        List_to_return.append(dictionary)

    final_content = [email, List_to_return]

    return str(final_content)


@app.route("/retrieve/survey/<email>/<survey_id>/results", methods=['GET'])
#User must be logged in, and must also be retreiving data on their own surveys

# Retrieve specific survey results
def retrieveSurveyResults(email, survey_id):
    multiple_choice = {}
    short_response = []
    Database = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ferdaosm50313245!",
        database="test_db"
    )
    # Access the Database
    mydb = Database
    mycursor = mydb.cursor()

    query = "SELECT * FROM Response WHERE email = %s AND survey_id = %s"
    values = (email, survey_id)

    # # Execute our MySQL Query to get what we want
    mycursor.execute(query, values)

    # fetch all the matching rows 
    result = mycursor.fetchall()

    for row in result:
        Question_id = row[1]

        print(row)
    

    return "testing retrieval of responses"

@app.route('/retrieve/PublicSurveys')
# User does NOT have to be logged in to see public surveys
def retrievePublicSurveys():
    List_to_return = []
    Database = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ferdaosm50313245!",
        database="test_db"
    )
    # Access the Database
    mydb = Database
    mycursor = mydb.cursor()

    # Get all of the surveys from the 'Surveys' table.
    query = "SELECT * FROM Surveys"
    # Execute our MySQL Query to get what we want
    mycursor.execute(query)
    # fetch all the matching rows 
    result = mycursor.fetchall()
    # Get todyas date to check whether or not the survey has expired.
    todays_date = date.today()

    # row format = [id, email, title, description, created_on, expire, surveys_id]
    for row in result:
        # This will be the dictionary that we use to add in all Surveys that have not expired
        Dictionary_to_append = {}
        # If the expiration date has not passed, then we add it to a list that we will return.
        expiration_date = row[5]

        if expiration_date > todays_date:
            survey_id = row[6]
            survey_title = row[2]
            survey_description = row[3]
            Dictionary_to_append['survey_id'] = survey_id
            Dictionary_to_append['survey_title'] = survey_title
            Dictionary_to_append['survey_description'] = survey_description
            List_to_return.append(Dictionary_to_append)

    return str(List_to_return)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
    #app.run(debug = True) # Set to false for production
