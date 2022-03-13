import db_connector
from application import datetime, date

def retrieveSurveysUsers(email):
    List_to_return = []
    
    # Access the Database
    mydb = db_connector.dbConnector("root","")
    mycursor = mydb.cursor()

    # Select only the rows that have our requested "email" 
    query = "SELECT * FROM Surveys WHERE email = %s"
    user_email = (email, )

    # Execute our MySQL Query to get what we want
    mycursor.execute(query, user_email)
    # fetch all the matching rows 
    result = mycursor.fetchall()
    
    # loop through the rows that have only the requested email in them and 
    # row format = [id, email, title, description, created_on, expire, surveys_id]
    for row in result:
        dictionary = {}
        # Get the surveys_id, this will act as a Value
        surveys_id = row[6]
        # Get the survey_title, this will act as a Key
        survey_title = row[2]
        dictionary[survey_title] = surveys_id
        # Append the created dictionary to the list that we are going to return
        List_to_return.append(dictionary)

    final_content = [email, List_to_return]

    return str(final_content)

def retrieveSurveyResults(email, survey_id):
    multiple_choice = {}
    short_response = []

    # Access the Database
    mydb = db_connector.dbConnector("root","")
    mycursor = mydb.cursor()

    query = "SELECT * FROM Response WHERE email = %s AND survey_id = %s"
    values = (email, survey_id)

    # # Execute our MySQL Query to get what we want
    mycursor.execute(query, values)

    # fetch all the matching rows 
    result = mycursor.fetchall()

    for row in result:
        Question_id = row[1]

        print(row)
    

    return "testing retrieval of responses"

def retrievePublicSurveys():
    List_to_return = []

    # Access the Database
    mydb = db_connector.dbConnector("root","")
    mycursor = mydb.cursor()

    # Get all of the surveys from the 'Surveys' table.
    query = "SELECT * FROM Surveys"
    # Execute our MySQL Query to get what we want
    mycursor.execute(query)
    # fetch all the matching rows 
    result = mycursor.fetchall()
    # Get todyas date to check whether or not the survey has expired.
    todays_date = date.today()

    # row format = [id, email, title, description, created_on, expire, surveys_id]
    for row in result:
        # This will be the dictionary that we use to add in all Surveys that have not expired
        Dictionary_to_append = {}
        # If the expiration date has not passed, then we add it to a list that we will return.
        expiration_date = row[5]

        if expiration_date > todays_date:
            survey_id = row[6]
            survey_title = row[2]
            survey_description = row[3]
            Dictionary_to_append['survey_id'] = survey_id
            Dictionary_to_append['survey_title'] = survey_title
            Dictionary_to_append['survey_description'] = survey_description
            List_to_return.append(Dictionary_to_append)

    return str(List_to_return)

