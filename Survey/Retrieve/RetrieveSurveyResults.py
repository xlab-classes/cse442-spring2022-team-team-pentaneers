import db_connector

def retrieveSurveyResults(email, surveys_id):
    final_list = []

    # Access the Database
    mydb = db_connector.dbConnector()
    mycursor = mydb.cursor()
    # Access the Surveys table to get the specific Survey for the user.
    query = "SELECT * FROM Surveys WHERE email = %s AND surveys_id = %s"
    values = (email, surveys_id)
    mycursor.execute(query, values)
    result = mycursor.fetchall()
    # Getting the title of the survey
    survey_title = result[0][2]
    survey_id = result[0][0]

    query = "SELECT * FROM Response WHERE survey_id = %s"
    values = (survey_id, )
    mycursor.execute(query, values)
    # fetch all the matching rows 
    result = mycursor.fetchall()

    for row in result:
        new_list = []
        new_dic = {}
        # row format: [response_id, question_id, survey_id, short_answer, multiple_choice_answer, email]
        question_number = row[1]
        short_answer_response = row[3]
        multiple_choice_response = row[4]
        responder_email = row[5]
        new_list.append(responder_email)
        new_dic['question_number'] = question_number
        # If short_response == None, that means that the question at the moment is Multiple Choice
        if row[3] == None:
            new_dic['multiple_choice_response'] = int(multiple_choice_response)
        else:
            new_dic['short_answer_response'] = short_answer_response
        
        new_list.append(new_dic)

        final_list.append(new_list)
    

    return str(final_list)