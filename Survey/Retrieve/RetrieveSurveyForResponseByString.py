import db_connector
from Survey.Status import Auto
from datetime import datetime
def retrieve(surveys_id, unique_string):

    # Access the Database
    Auto.autoClose()
    mydb = db_connector.dbConnector()
    mycursor = mydb.cursor()
    # Access the Surveys table to get the specific Survey for the user.
    query = "SELECT * FROM Surveys WHERE surveys_id = %s AND unique_string = %s"
    values = (surveys_id, unique_string)
    mycursor.execute(query, values)
    survey = mycursor.fetchall()
    print("This is the survey: ", survey, '\n')
    if len(survey) == 0:
        return None
    
    status = survey[0][10]

    if status == 'close':
        return None

    survey_id = survey[0][0]
    

    query = "SELECT * FROM Questions WHERE survey_id = %s"
    value = (survey_id, )
    # Execute our MySQL Query to get what we want
    mycursor.execute(query, value)
    # Fetch all Questions belonging to the requested Survey
    survey_questions = mycursor.fetchall()
    print("These are the survey questions: ", survey_questions, '\n')


    if len(survey) == 0:
        # Make this a 404 message
        return None
        
    survey = survey[0]
    
    # Appending the survey information ('survey' index 1 = email, 'survey' index 2 = title, 'survey' index 3 = description)
    list_to_return = [survey[2], survey[3]]


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
