
from Survey.Retrieve import parseSurveyQuestions, RetrieveSurveyById
import db_connector
import datetime

def modifySurvey(id, data):

    # Access the Database
    mydb = db_connector.dbConnector()
    mycursor = mydb.cursor()

    # Extract the title, description, expired_date, and visibility in the recieved data.
    new_survey_title = data['title'].replace(";", "")
    new_survey_description = data['description'].replace(";", "")
    new_survey_questions = data['questions']
    new_survey_expiration_date = data['expired_date'].replace(";", "")
    if new_survey_expiration_date != '':
        new_survey_expiration_date = datetime.datetime.strptime(new_survey_expiration_date,"%Y-%m-%d").date()
    new_survey_visibility = data['visibility'].replace(";", "")

    # check survey exists
    email = data['email']
    exists = RetrieveSurveyById.retrieveSurveyById(id, email)
    if (exists == "Error 404, This survey does not exist!"):
        return "survey not exists"

    # Update title, description, expired_date, and visibility in Surveys if any information is changed.

    
    # -------------------------Update the survey title------------------------------
    # Length of the survey title should NOT be 0 and we will not allow ';' for now (Security Issue)
    if len(new_survey_title) != 0:
        update_survey_title = "UPDATE Surveys SET title = %s WHERE id = %s"
        val = (new_survey_title, id)
        mycursor.execute(update_survey_title, val)
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected for title")

    # -----------------Update the description if anything has changed---------------
    update_survey_description = "UPDATE Surveys SET description = %s WHERE id = %s"
    val = (new_survey_description, id)
    mycursor.execute(update_survey_description, val)
    mydb.commit()
    print(mycursor.rowcount, "record(s) affected for description")

    # ----------------Update the expiration date-------------------------
    if isinstance(new_survey_expiration_date, datetime.date):
        update_expiraton_date = "UPDATE Surveys SET expired_on = %s WHERE id = %s"
        val = (new_survey_expiration_date, id)
        mycursor.execute(update_expiraton_date, val)
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected for expiration_date")

    # ---------------Update the visibility if it changed------------------
    update_visibilty = "UPDATE Surveys SET visibility = %s WHERE id = %s"
    val = (new_survey_visibility, id)
    mycursor.execute(update_visibilty, val)
    mydb.commit()
    print(mycursor.rowcount, "record(s) affected for visibility")

    #---------Gathering all Questions from the survey---------

    query = "SELECT * FROM Questions WHERE survey_id = %s"
    value = (id, )
    # Execute our MySQL Query to get what we want
    mycursor.execute(query, value)
    database_survey_questions = mycursor.fetchall()

    #------------If there are no changes, just return with a message----------------------
    
    old_survey_questions = parseSurveyQuestions.parseSurveyQuestions(database_survey_questions)

    if str(old_survey_questions) == str(new_survey_questions):
        return "No Question Changes were made!"

    #------------------------Update Questions------------------------------ 


    # Add all of the new questions back
    questionnumberList=[]
    question_id = 0
    relation_id = len(old_survey_questions)
    # Looping through the newly (possibly) modified survey
    for question in new_survey_questions:

        new_question_title = question[0]
        new_question_type = question[1]
        new_question_options = question[2]
        question_id += 1
        
        # If the User has not added any questions, then we can safely assume they have modified something
        if question_id < len(old_survey_questions)+1:
            questionnumberList.append(question_id)
            
            # Checking to see if the question title has changed
            if new_question_title != old_survey_questions[question_id-1][0]:
            
                update_question_title = "UPDATE Questions SET question_title = %s WHERE question_id = %s"
                val = (new_question_title, question_id)
                mycursor.execute(update_question_title, val)
                mydb.commit()
                # Delete from Response table
                response_query = "DELETE FROM Response WHERE question_id = %s AND survey_id = %s"
                values = (question_id, id)
                mycursor.execute(response_query, values)
                mydb.commit()
                print(mycursor.rowcount, "record(s) affected for survey_title in Questions")
            
            # Checking to see if the question type has changed
            if new_question_type != old_survey_questions[question_id-1][1]:
                update_question_type = "UPDATE Questions SET question_type = %s WHERE question_id = %s"
                val = (new_question_type, question_id)
                mycursor.execute(update_question_type, val)
                mydb.commit()
                print(mycursor.rowcount, "record(s) affected for survey_type in Questions")

                # Checking to see if the question options have changed
                if new_question_options != old_survey_questions[question_id-1][2]:
                    if new_question_options is None:
                        update_question_options = "UPDATE Questions SET options = %s WHERE question_id = %s"
                        val = (new_question_options, question_id)
                        mycursor.execute(update_question_options, val)
                        mydb.commit()
                    else:
                        index=0
                        options=""
                        for choice in new_question_options:
                            index+=1
                            options+=str(index)+":"+choice+";"
                        update_question_options = "UPDATE Questions SET options = %s WHERE question_id = %s"
                        val = (options, question_id)
                        mycursor.execute(update_question_options, val)
                        mydb.commit()
                        print(mycursor.rowcount, "record(s) affected for survey_options in Questions")

                    # Delete from Response table
                    response_query = "DELETE FROM Response WHERE question_id = %s AND survey_id = %s"
                    values = (question_id, id)
                    mycursor.execute(response_query, values)
                    mydb.commit()

            if new_question_type == old_survey_questions[question_id-1][1]:
                # Checking to see if the question options have changed
                if new_question_options != old_survey_questions[question_id-1][2]:
                    if new_question_options is None:
                        update_question_options = "UPDATE Questions SET options = %s WHERE question_id = %s"
                        val = (new_question_options, question_id)
                        mycursor.execute(update_question_options, val)
                        mydb.commit()
                    else:
                        index=0
                        options=""
                        for choice in new_question_options:
                            index+=1
                            options+=str(index)+":"+choice+";"
                        update_question_options = "UPDATE Questions SET options = %s WHERE question_id = %s"
                        val = (options, question_id)
                        mycursor.execute(update_question_options, val)
                        mydb.commit()
                        print(mycursor.rowcount, "record(s) affected for survey_options in Questions")

                    # Delete from Response table
                    response_query = "DELETE FROM Response WHERE question_id = %s AND survey_id = %s"
                    values = (question_id, id)
                    mycursor.execute(response_query, values)
                    mydb.commit()

                update_question_type = "UPDATE Questions SET question_type = %s WHERE question_id = %s"
                val = (new_question_type, question_id)
                mycursor.execute(update_question_type, val)
                mydb.commit()
                print(mycursor.rowcount, "record(s) affected for survey_type in Questions")
        # If the User has ADDED more questions, then we can safely insert more questions to the Database
        if question_id > len(old_survey_questions) and question_id <= len(new_survey_questions):

            if(new_question_options is None):
                sql = "Insert into Questions (survey_id, question_id, question_title, question_type) values (%s,%s,%s,%s)"
                val = (id, question_id, new_question_title, new_question_type)
                mycursor.execute(sql, val)
                mydb.commit()
            else:
                index=0
                options=""
                for choice in question[2]:
                    index+=1
                    options+=str(index)+":"+choice+";"
                sql = "Insert into Questions (survey_id, question_id, question_title, question_type, options) values (%s,%s,%s,%s,%s)"
                val = (id,question_id, new_question_title, new_question_type, options)
                mycursor.execute(sql, val)
                mydb.commit()
            
    #insert into Survey_Questions
    for question in range(len(old_survey_questions), len(new_survey_questions)):
        relation_id += 1
        sql = "Insert into Survey_Questions (question_id, survey_id) values (%s,%s)"
        val = (question+1, id)
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

    return str(response)