import datetime
import db_connector
from datetime import datetime

from Survey.Status import Auto
from db_initial import initial
import random
import string
from flask import request

def survey(data):
    email=data['email']
    title=data['title']
    description=data['description']
    questions=data['questions']
    expired=data['expired_date']
    if(expired != ''):
        expired=datetime.strptime(expired, "%Y-%m-%dT%H:%M")
        time_stamp = int(datetime.timestamp(expired))
        expired=time_stamp
    if (expired == ''):
        expired = None

    visibility=data['visibility']
    
    # Generate a unique url for the survey so that it can be shared around.
    letters = string.ascii_letters
    unique_string = ''.join(random.choice(letters) for i in range(5))
    print(unique_string)
    #get current date,YYYY-MM-DD format
    created_date=datetime.now()
    created_date=int(datetime.timestamp(created_date))

    #var need to be calculated
    countrow = -1
    id = -1
    surveys_id = -1
    question_id = 0 #id in Questions
    relation_id = -1

    # connect database
    mydb = db_connector.dbConnector()
    mycursor = mydb.cursor()

    # create tables if they don't exist
    initial()

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
    #Generate the full unique url
    unique_url = request.host_url + 'survey/respond/' + str(surveys_id) + '/' + unique_string 
    #insert data into Surveys
    sql="Insert into Surveys (email, title, description, created_on, expired_on, surveys_id,visibility,unique_url,unique_string,status) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(email,title,description,created_date,expired,surveys_id,visibility,unique_url,unique_string,"open")
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
    Auto.autoClose()
    mydb.close()
    return id