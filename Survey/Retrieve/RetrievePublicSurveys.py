import db_connector
from datetime import datetime

from Survey.Status import Auto


def retrievePublicSurveys():
    Auto.autoClose()
    List_to_return = []

    # Access the Database
    mydb = db_connector.dbConnector()
    mycursor = mydb.cursor()

    # Get all of the surveys from the 'Surveys' table.
    query = "SELECT * FROM Surveys"
    # Execute our MySQL Query to get what we want
    mycursor.execute(query)
    # fetch all the matching rows 
    result = mycursor.fetchall()
    # Get todyas date to check whether or not the survey has expired.
    todays_date = datetime.now()
    todays_date = int(datetime.timestamp(todays_date))

    # row format = [id, email, title, description, created_on, expire, surveys_id, visibility]
    for row in result:
        # This will be the list that we use to add in all Surveys that have not expired
        list_to_append = []
        # If the expiration date has not passed, then we add it to a list that we will return.
        expiration_date = row[5]
        
        visibility = row[7]
        status = row[10]

        if expiration_date == None and visibility == 'public' and (status == 'open' or status == None):
            survey_id = row[0]
            survey_title = row[2]
            survey_description = row[3]
            survey_url = row[8]
            list_to_append.append(survey_title)
            list_to_append.append(survey_description)
            list_to_append.append(survey_url)
            List_to_return.append(list_to_append)

        if expiration_date != None:
            if expiration_date > todays_date and visibility == 'public' and (status == 'open' or status == None):
                survey_id = row[0]
                survey_title = row[2]
                survey_description = row[3]
                survey_url = row[8]
                list_to_append.append(survey_title)
                list_to_append.append(survey_description)
                list_to_append.append(survey_url)
                List_to_return.append(list_to_append)
                
    if len(List_to_return) == 0:
        return None
            

    return List_to_return