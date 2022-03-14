import datetime
import json
import db_connector
from datetime import date
def response(data):
    responses = data['response']
    survey_id = data['survey_id']
    email = data['email']
    question_number = 0

    # connect database
    mydb = db_connector.dbConnector("root")
    mycursor = mydb.cursor()

    sql = "create table if not exists Response (response_id int AUTO_INCREMENT PRIMARY KEY, question_id int, survey_id int,short_answer varchar(255), multiple_choice_answer varchar(255), email varchar(255))"
    mycursor.execute(sql)
    mydb.commit()

    # insert each response
    for response in responses:
        question_number += 1  # question_id in Questions
        question_type = response[0]
        answer = response[1]
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