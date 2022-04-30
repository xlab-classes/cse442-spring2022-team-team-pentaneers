from Survey.Status import Auto
from db_connector import dbConnector

def surveyID(email, surveys_id):
    Auto.autoClose()
    # Access the Database
    mydb = dbConnector()
    mycursor = mydb.cursor()
    # Getting the specific survey that belongs to the user
    query = "SELECT * FROM Surveys WHERE surveys_id = %s AND email = %s"
    value = (surveys_id, email)
    mycursor.execute(query, value)
    # Fetch the survey information belonging to the requested Survey
    survey = mycursor.fetchall()

    if len(survey) > 0:
        survey_id = survey[0][0]
        return survey_id
    
    return None

    


def surveysID(email, survey_id):
    # Access the Database
    mydb = dbConnector()
    mycursor = mydb.cursor()
    # Getting the specific survey that belongs to the user
    query = "SELECT * FROM Surveys WHERE id = %s AND email = %s"
    value = (survey_id, email)
    mycursor.execute(query, value)
    # Fetch the survey information belonging to the requested Survey
    survey = mycursor.fetchall()

    surveys_id = survey[0][6]

    return surveys_id

def latestSurveysID(email):
    # Access the Database
    mydb = dbConnector()
    mycursor = mydb.cursor()
    # Getting the specific survey that belongs to the user
    query = "SELECT MAX(surveys_id) AS maximum from Surveys WHERE email = %s"
    value = (email, )
    mycursor.execute(query, value)
    # Fetch the survey information belonging to the requested Survey
    survey = mycursor.fetchall()
    mycursor.close()

    return survey[0][0]

def get_surveys_id_by_uniqueString(unique_string):
    # Access the Database
    mydb = dbConnector()
    mycursor = mydb.cursor()
    # Getting the specific survey that belongs to the user
    query = "SELECT * FROM Surveys WHERE  unique_string= %s"
    value = (unique_string, )
    mycursor.execute(query, value)
    # Fetch the survey information belonging to the requested Survey
    survey = mycursor.fetchall()
    if len(survey) == 0:
        return None
        
    return survey[0][0]