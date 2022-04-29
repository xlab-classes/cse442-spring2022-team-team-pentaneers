from Survey.Status import Auto
from db_connector import dbConnector

def get():
    responses = []
    # Access the Database
    mydb = dbConnector()
    mycursor = mydb.cursor()
    
    all_public_surveys = public_surveys()

    for public_survey in all_public_surveys:
        query = "SELECT * FROM Response WHERE survey_id=%s"
        specific_survey_id = (public_survey[0], )
        mycursor.execute(query, specific_survey_id)
        responses += mycursor.fetchall()
    
    # If there are no responses at all, we will return None
    print("These are all of the responses: ", responses)
    if len(responses) == 0:
        return None

    if len(responses) != 0:
        response_counters = {}

        for response in responses:
            # index 2 holds the survey id
            surveys_id = response[2]
            # index 1 holds the question number
            question_number = response[1]
            if surveys_id in response_counters and question_number == 1:
                response_counters[surveys_id] += 1
                
            if surveys_id not in response_counters:
                response_counters[surveys_id] = 1

        popular_survey = max(response_counters, key=response_counters.get)

        query = "SELECT * FROM Surveys WHERE id=%s"
        value = (popular_survey, )
        mycursor.execute(query, value)

        popular_survey = mycursor.fetchall()
        
        mycursor.close()
        popular_survey = popular_survey[0]
        # Survey info will be in the format of [title, description, URL]
        survey_info = [popular_survey[2], popular_survey[3], popular_survey[8]]
        return survey_info

''' This function retrieves all of the open and public surveys'''
def public_surveys():
    # Access the Database
    mydb = dbConnector()
    mycursor = mydb.cursor()
    query = "SELECT * FROM Surveys WHERE visibility=%s AND status=%s"
    value = ('public','open')
    mycursor.execute(query, value)
    all_public_surveys = mycursor.fetchall()
    return all_public_surveys