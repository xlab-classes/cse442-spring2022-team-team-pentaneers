import Database

# Retrieve survey for coordinators by using survey_id
def retrieveSurveyById (survey_id, email):
    # Access the Database
    mydb = Database.dbConnector("root","")
    mycursor = mydb.cursor()
    # Getting the specific survey that belongs to the user
    query = "SELECT * FROM Surveys WHERE id = %s AND email = %s"
    value = (survey_id, email)
    mycursor.execute(query, value)
    # Fetch the survey information belonging to the requested Survey
    survey = mycursor.fetchall()
    survey = survey[0]

    # Fetch the questions for the requested Survey
    query = "SELECT * FROM Questions WHERE survey_id = %s"
    value = (survey_id, )
    # Execute our MySQL Query to get what we want
    mycursor.execute(query, value)
    survey_questions = mycursor.fetchall()

    # Appending the survey information ('survey' index 0 = id,'survey' index 1 = email, 'survey' index 2 = title, 'survey' index 3 = description, 'survey' index 5 = expired_on)
    list_to_return = [survey[0], survey[1], survey[2], survey[3], survey[5]]

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
