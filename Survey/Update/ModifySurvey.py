
from Survey.Retrieve import parseSurveyQuestions, RetrieveSurveyById

import db_connector
import datetime

def modifySurvey(id, data):

    # Access the Database
    mydb = db_connector.dbConnector()
    mycursor = mydb.cursor()

    # Extract the title, description, expired_date, and visibility in the recieved data.
    survey_title = data['title'].replace(";", "")
    survey_description = data['description'].replace(";", "")
    survey_questions = data['questions']
    survey_expiration_date = data['expired_date'].replace(";", "")
    survey_expiration_date = datetime.datetime.strptime(survey_expiration_date,"%Y-%m-%d").date()
    print(survey_expiration_date)
    survey_visibility = data['visibility'].replace(";", "")

    # Update title, description, expired_date, and visibility in Surveys if any information is changed.

    
    # -------------------------Update the survey title------------------------------
    # Length of the survey title should NOT be 0 and we will not allow ';' for now (Security Issue)
    if len(survey_title) != 0:
        update_survey_title = "UPDATE Surveys SET title = %s WHERE id = %s"
        val = (survey_title, id)
        mycursor.execute(update_survey_title, val)
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected for title")

    # -----------------Update the description if anything has changed---------------
    update_survey_description = "UPDATE Surveys SET description = %s WHERE id = %s"
    val = (survey_description, id)
    mycursor.execute(update_survey_description, val)
    mydb.commit()
    print(mycursor.rowcount, "record(s) affected for description")

    # ----------------Update the expiration date-------------------------
    if isinstance(survey_expiration_date, datetime.date):
        update_expiraton_date = "UPDATE Surveys SET expired_on = %s WHERE id = %s"
        val = (survey_expiration_date, id)
        mycursor.execute(update_expiraton_date, val)
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected for expiration_date")

    # ---------------Update the visibility if it changed------------------
    update_visibilty = "UPDATE Surveys SET visibility = %s WHERE id = %s"
    val = (survey_visibility, id)
    mycursor.execute(update_visibilty, val)
    mydb.commit()
    print(mycursor.rowcount, "record(s) affected for visibility")

    #---------If no questions were updated, leave everything as is---------

    query = "SELECT * FROM Questions WHERE survey_id = %s"
    value = (id, )
    # Execute our MySQL Query to get what we want
    mycursor.execute(query, value)
    database_survey_questions = mycursor.fetchall()

    #------------If there are no changes, just return with a message----------------------
    
    parse_question = parseSurveyQuestions.parseSurveyQuestions(database_survey_questions)
    if parse_question == str(survey_questions):
        return "No Question Changes were made!"

    #------------------------Update Questions------------------------------ 

    # Delete all questions and relations to questions (Questions & Survey_Questions & Responses)

    # Delete from Questions
    question_query = "DELETE FROM Questions WHERE survey_id = %s"
    values = (id,)
    mycursor.execute(question_query, values)
    mydb.commit()
    print("Questions Table: ", mycursor.rowcount, "record(s) deleted")

    # Delete from Survey_Question table
    survey_question_query = "DELETE FROM Survey_Questions WHERE survey_id = %s"
    values = (id,)
    mycursor.execute(survey_question_query, values)
    mydb.commit()
    print("Survey_Questions: ", mycursor.rowcount, "record(s) deleted")

    # Delete from Response table
    response_query = "DELETE FROM Response WHERE survey_id = %s"
    values = (id, )
    mycursor.execute(response_query, values)
    mydb.commit()
    print("Response Table: ", mycursor.rowcount, "record(s) deleted")

    # Add all of the new questions back
    questionnumberList=[]
    question_id = 0
    # insert data into Questions table
    for question in survey_questions:
        question_title=question[0].replace(";", "")
        question_type=question[1].replace(";", "")
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

    #insert into Survey_Questions table
    for question in questionnumberList:
        sql = "Insert into Survey_Questions ( question_id, survey_id) values (%s,%s)"
        val = (question,id)
        mycursor.execute(sql, val)
        mydb.commit()
    
    query = "SELECT * FROM Surveys WHERE id = %s"
    value = (id, )
    mycursor.execute(query, value)
    # Fetch the survey information belonging to the requested Survey
    survey = mycursor.fetchall()
    
    email = survey[0][1]

    mydb.close()

    response = RetrieveSurveyById.retrieveSurveyById(id, email)

    return response