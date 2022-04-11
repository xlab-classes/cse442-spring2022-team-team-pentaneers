import db_connector
from Survey.Retrieve import RetrieveSurveyById
from flask import request


def deleteSurvey(email, id):

    # Access the Database
    mydb = db_connector.dbConnector()
    mycursor = mydb.cursor()

    exists = RetrieveSurveyById.retrieveSurveyById(id, email)
    if (exists == "Error 404, This survey does not exist!"):
        return "survey not exists"

    # Select only the rows that have our requested "email" 
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
    query = "DELETE FROM Response WHERE survey_id = %s"
    values = (id, )
    mycursor.execute(query, values)
    mydb.commit()
    print("Response Table: ", mycursor.rowcount, "record(s) deleted")
    # Retrieve all surveys
    # Select only the rows that have our requested "email" 
    query = "SELECT * FROM Surveys WHERE email = %s"
    user_email = (email, )

    # Execute our MySQL Query to get what we want
    mycursor.execute(query, user_email)
    # fetch all the matching rows 
    result = mycursor.fetchall()

    counter = 1
    if len(result) != 0: 
        for survey in result:
            survey_id = survey[0]
            update_surveys_id = "UPDATE Surveys SET surveys_id = %s WHERE id = %s"
            val = (counter, survey_id)
            mycursor.execute(update_surveys_id, val)
            mydb.commit()
            unique_string = survey[9]
            #Generate the full unique url
            unique_url = request.host_url + 'survey/respond/' + str(counter) + '/' + unique_string
            update_unique_url = "UPDATE Surveys SET unique_url = %s WHERE id = %s"
            val = (unique_url, survey_id)
            mycursor.execute(update_unique_url, val)
            mydb.commit()
            counter+=1
        

    return ("Survey has been deleted for email: {} with survey_id = {}").format(email, id)