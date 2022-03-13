import datetime
import json
import db_connector
from datetime import date
def response(data):
    responses = data['response']
    survey_id = data['survey_id']
    email = data['email']

    # connect database
    mydb = db_connector.dbConnector("root", "50310786")
    mycursor = mydb.cursor()

    sql = "create table if not exists Response (response_id int AUTO_INCREMENT PRIMARY KEY, question_id int, survey_id int,short_answer varchar(255), multiple_choice_answer varchar(255), email varchar(255))"
    mycursor.execute(sql)
    mydb.commit()

    # insert each response
    for response in responses:
        question_number = response[0]  # question_id in Questions
        question_type = response[1]
        answer = response[2]
        if (question_type == "Short Response"):
            sql = "Insert into Response (question_id, survey_id, short_answer, email) values (%s,%s,%s,%s)"
            val = (question_number, survey_id, answer, email)
            mycursor.execute(sql, val)
            mydb.commit()
        else:
            sql = "Insert into Response (question_id, survey_id, multiple_choice_answer, email) values (%s,%s,%s,%s)"
            val = (question_number, survey_id, int(answer), email)
            mycursor.execute(sql, val)
            mydb.commit()

    mydb.close()
    return json.dumps(survey_id)