import datetime
import json

from flask import Flask,request
import mysql.connector
from datetime import date

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

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database = "testdb"
    )
    mycursor = mydb.cursor()

    # create table Surveys if not exists
    '''
    sql = "drop TABLE IF EXISTS Surveys"
    mycursor.execute(sql)
    mydb.commit()
    '''
    sql = "CREATE TABLE IF NOT EXISTS Surveys (id int, email varchar(255), title varchar(255), description varchar(255), created_on DATE, expired_on Date, surveys_id int)"
    mycursor.execute(sql)
    mydb.commit()

    # create table Survey_Questions if not exists
    '''
    sql = "drop TABLE IF EXISTS Survey_Questions"
    mycursor.execute(sql)
    mydb.commit()
    '''
    sql = "CREATE TABLE IF NOT EXISTS Survey_Questions (id int, question_id int, survey_id int)"
    mycursor.execute(sql)
    mydb.commit()

    # create table Questions if not exists
    '''
    sql = "drop TABLE IF EXISTS Questions"
    mycursor.execute(sql)
    mydb.commit()
    '''
    sql = "CREATE TABLE IF NOT EXISTS Questions (id int, survey_id int, question_id int, question_title varchar(255), question_type varchar(255), options varchar(255))"
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

    # for Questions table
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
        question_number=question[0] #question_id in Questions
        question_title=question[1]
        question_type=question[2]
        question_id += 1
        questionnumberList.append(question_number)
        if(question[3] is None):
            sql = "Insert into Questions (id, survey_id, question_id, question_title, question_type) values (%s,%s,%s,%s,%s)"
            val = (question_id, id,question_number, question_title, question_type)
            mycursor.execute(sql, val)
            mydb.commit()
        else:
            index=0
            options=""
            for choice in question[3]:
                index+=1
                options+=str(index)+":"+choice+";"
            sql = "Insert into Questions (id, survey_id, question_id, question_title, question_type, options) values (%s,%s,%s,%s,%s,%s)"
            val = (question_id, id,question_number, question_title, question_type, options)
            mycursor.execute(sql, val)
            mydb.commit()

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
    for question in questionnumberList:
        relation_id += 1
        sql = "Insert into Survey_Questions (id, question_id, survey_id) values (%s,%s,%s)"
        val = (relation_id,question,id)
        mycursor.execute(sql, val)
        mydb.commit()

    # used for testing values are inserted correctly
    '''
    returnstring="Surveys: "
    sql = "select * from Surveys"
    #val = (id,)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        returnstring+=str(x)
        returnstring+='\n'
    returnstring += '\n'
    returnstring+="Survey_Questions: "
    sql = "select * from Survey_Questions"
    #val = (id,)
    mycursor.execute(sql)
    # mydb.commit()
    myresult = mycursor.fetchall()
    for x in myresult:
        returnstring += str(x)
        returnstring += '\n'
    #returnstring+="Surveys: "+
    returnstring += '\n'
    returnstring += "Questions: "
    #for questionid in questionidList:
    sql = "select * from Questions"
    #val=(questionid,)
    # val = (relation_id, question, id)
    mycursor.execute(sql)
    # mydb.commit()
    myresult = mycursor.fetchall()
    for x in myresult:
        returnstring += str(x)
        returnstring += '\n'
    '''
    mydb.close()

    return json.dumps(id)
    #pass

@app.route("/signup", methods=['POST'])
def createAccount():
    data=json.loads(request.get_data(as_text=True))
    email=data['email']
    password=data['password']
    created_date = date.today()
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="testdb"
    )
    mycursor = mydb.cursor()
    '''
    sql = "drop table if exists Users"
    mycursor.execute(sql)
    mydb.commit()
    '''
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
    #mydb.commit()

    # return tuples in Users(used for testing)
    '''
    sql = "select * from Users"
    #val = (email,)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    returnid=""
    for x in myresult:
        returnid += str(x)
    '''
    mydb.close()
    return json.dumps(returnid)
    #pass

@app.route("/submitResponse", methods=['POST'])
def createResponse():

    #get body of the request
    data=json.loads(request.get_data(as_text=True))
    responses=data['response']
    survey_id=data['survey_id']
    email=data['email']
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="testdb"
    )
    mycursor = mydb.cursor()
    sql = "create table if not exists Response (response_id int AUTO_INCREMENT PRIMARY KEY, question_id int, survey_id int,short_answer varchar(255), multiple_choice_answer varchar(255), email varchar(255))"
    mycursor.execute(sql)
    mydb.commit()

    #insert each response
    print(responses)
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

    #return tuples in Response(used for testing)
    '''
    sql = "select * from Response"
    # val = (email,)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    returnid = ""
    for x in myresult:
        returnid += str(x)
    '''
    mydb.close()
    return json.dumps(survey_id)
@app.route("/survey/delete/<email>/<id>", methods = ['DELETE'])
def deleteSurvey(email, id):
    print(email)
    print(id)
    Database = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="testdb"
    )
    # Access the Database
    mydb = Database
    mycursor = mydb.cursor()
    # Select only the rows that have our requested "email" 
    
    query = "SELECT * FROM Surveys WHERE email = %s AND id = %s"
    values = (email, id)
    
    # Execute our MySQL Query to get what we want
    mycursor.execute(query, values)
    # fetch all the matching rows 
    result = mycursor.fetchall()
    
    print(result)

    # Delete from Surveys table
    query = "DELETE FROM Surveys WHERE email = %s AND id = %s"
    values = (email, id)
    mycursor.execute(query, values)
    mydb.commit()
    print("Surveys Table: ", mycursor.rowcount, "record(s) deleted")
   
    # Delete from Questions
    query = "DELETE FROM Questions WHERE survey_id = %s"
    values = (id,)
    mycursor.execute(query, values)
    mydb.commit()
    print("Questions Table: ", mycursor.rowcount, "record(s) deleted")

    # Delete from Survey_Question table
    query = "DELETE FROM Survey_Questions WHERE survey_id = %s"
    values = (id,)
    mycursor.execute(query, values)
    mydb.commit()
    print("Survey_Questions: ", mycursor.rowcount, "record(s) deleted")

    # Delete from Response table
    query = "DELETE FROM Response WHERE email = %s AND survey_id = %s"
    values = (email, id)
    mycursor.execute(query, values)
    mydb.commit()
    print("Response Table: ", mycursor.rowcount, "record(s) deleted")
    
    
    return ("Survey has been deleted for email: {} with survey_id = {}").format(email, id)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
    #app.run(debug = True) # Set to false for production
