import Database

# Complete surveys (Action)
def retrieveSurveyForResponse(survey_id):

    # Access the Database
    mydb = Database.dbConnector("root","")
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
    survey = survey[0]
    
    # Appending the survey information ('survey' index 1 = email, 'survey' index 2 = title, 'survey' index 3 = description)
    list_to_return = [survey[1], survey[2], survey[3]]


    for row in survey_questions:
        dic = {}
        question_number = 'question_' + str(row[2])
        question_title =row[3]
        question_type = row[4]
        choice = row[5]
        question_info = [question_title, question_type, choice]
        dic[question_number] = question_info
        list_to_return.append(dic)
        
    return str(list_to_return)