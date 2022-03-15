import datetime
import json
import db_connector
from datetime import date

def survey(data):
    
    email=data['email']
    title=data['title']
    description=data['description']
    questions=data['questions']
    expired=data['expired_date']
    expired=datetime.datetime.strptime(expired,"%Y-%m-%d").date()
    status=data['visibility']
    
    #get current date,YYYY-MM-DD format
    created_date=date.today()

    #var need to be calculated
    countrow = -1
    id = -1
    surveys_id = -1
    question_id = 0 #id in Questions
    relation_id = -1

    # connect database
    mydb = db_connector.dbConnector("root")
    mycursor = mydb.cursor()

    # create table Surveys if not exists
    sql = "CREATE TABLE IF NOT EXISTS Surveys (id int AUTO_INCREMENT PRIMARY KEY, email varchar(255), title varchar(255), description varchar(255), created_on DATE, expired_on Date, surveys_id int, visibility varchar(255))"
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
    sql="Insert into Surveys (email, title, description, created_on, expired_on, surveys_id,visibility) values (%s,%s,%s,%s,%s,%s,%s)"
    val=(email,title,description,created_date,expired,surveys_id,status)
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
        question_title=question[0]
        question_type=question[1]
        question_id += 1
        questionnumberList.append(question_id)
        if(question[2] is None):
            sql = "Insert into Questions (survey_id, question_id, question_title, question_type) values (%s,%s,%s,%s)"
            val = (id,question_id, question_title, question_type)
            mycursor.execute(sql, val)
            mydb.commit()
        else:
            index=0
            options=""
            for choice in question[2]:
                index+=1
                options+=str(index)+":"+choice+";"
            sql = "Insert into Questions (survey_id, question_id, question_title, question_type, options) values (%s,%s,%s,%s,%s)"
            val = (id,question_id, question_title, question_type, options)
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
    return id