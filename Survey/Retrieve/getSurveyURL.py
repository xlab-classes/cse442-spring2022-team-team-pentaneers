from db_connector import dbConnector
from Survey.Status import Auto

def get(email, surveys_id):
    Auto.autoClose()
    # Access the Database
    mydb = dbConnector()
    mycursor = mydb.cursor()
    # Getting the specific survey that belongs to the user
    query = "SELECT * FROM Surveys WHERE email = %s AND surveys_id = %s"
    value = (email, surveys_id)
    mycursor.execute(query, value)
    # Fetch the survey information belonging to the requested Survey
    survey = mycursor.fetchall()
    if len(survey) == 0:
        return("This survey could not be found, or it doesn't exists!")

    survey_url= survey[0][8]
    print("This is the survey url: ", survey_url)
    query = "SELECT status FROM Surveys WHERE email = %s AND surveys_id = %s"
    value = (email, surveys_id)
    mycursor.execute(query, value)
    survey = mycursor.fetchall()
    status=survey[0][0]
    if(status=="close"):
        return "survey closed"
    return survey_url