import Database


def retrieveSurveysUsers(email):
    List_to_return = []
    
    # Access the Database
    mydb = Database.dbConnector("root","")
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