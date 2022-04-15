import db_connector

# Complete surveys (Action)
from Survey.Status import Auto


def retrieveSurveyForResponse(survey_id):
    Auto.autoClose()
    # Access the Database
    mydb = db_connector.dbConnector()
    mycursor = mydb.cursor()

    query = "SELECT * FROM Questions WHERE survey_id = %s"
    value = (survey_id, )

    # Execute our MySQL Query to get what we want
    mycursor.execute(query, value)
    
    # Fetch all Questions belonging to the requested Survey
    survey_questions = mycursor.fetchall()
    

    query = "SELECT * FROM Surveys WHERE id = %s"
    value = (survey_id, )
   
    mycursor.execute(query, value)
    
    # Fetch the information belonging to the requested Survey
    survey = mycursor.fetchall()
    if len(survey) == 0:
        # Make this a 404 message
        return None
    survey = survey[0]
    
    # Appending the survey information ('survey' index 1 = email, 'survey' index 2 = title, 'survey' index 3 = description)
    list_to_return = [survey[1], survey[2], survey[3]]


    for row in survey_questions:
        dic = {}
        choice_list = []
        question_number = 'question_' + str(row[2])
        question_title =row[3]
        question_type = row[4]
        choice = row[5]
        if choice != None:
            choices = choice.split(";")
            choices.remove('')
            for choice in choices:
                start_choice = choice.find(":") + 1
                choice = choice[start_choice:]
                choice_list.append(choice)
            question_info = [question_title, question_type, choice_list]
        else:
            question_info = [question_title, question_type, choice]


        dic[question_number] = question_info
        list_to_return.append(dic)
        
    return list_to_return