import Database
from application import datetime, date


def retrievePublicSurveys():
    List_to_return = []

    # Access the Database
    mydb = Database.dbConnector("root","")
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