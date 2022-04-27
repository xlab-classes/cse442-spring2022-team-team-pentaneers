from Survey.Status import Auto
from db_connector import dbConnector

def get(email, surveys_id):
    # Access the Database
    mydb = dbConnector()
    mycursor = mydb.cursor()
    # Getting the specific survey that belongs to the user
    query = "SELECT * FROM Surveys WHERE surveys_id = %s AND email = %s"
    value = (surveys_id, email)
    mycursor.execute(query, value)
    # Fetch the survey information belonging to the requested Survey
    survey = mycursor.fetchall()
    return survey[0][5]
