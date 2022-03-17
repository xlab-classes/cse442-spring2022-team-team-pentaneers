import db_connector
from Survey.Retrieve import RetrieveSurveyById


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
    
    
    return ("Survey has been deleted for email: {} with survey_id = {}").format(email, id)