from db_connector import dbConnector

def surveyID(email, surveys_id):
    # Access the Database
    mydb = dbConnector()
    mycursor = mydb.cursor()
    # Getting the specific survey that belongs to the user
    query = "SELECT * FROM Surveys WHERE surveys_id = %s AND email = %s"
    value = (surveys_id, email)
    mycursor.execute(query, value)
    # Fetch the survey information belonging to the requested Survey
    survey = mycursor.fetchall()

    survey_id = survey[0][0]
    print("This is the survey: ", survey)

    return survey_id


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