import sys, os, inspect
import datetime
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
parent_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(1, parent_parent_dir)

from Back_End.Retrieve.RetrievePublicSurveys import retrievePublicSurveys
from db_connector import dbConnector


def test():
    mydb = dbConnector("root")
    mycursor = mydb.cursor()

    #get current date,YYYY-MM-DD format
    created_date = datetime.date.today()


    mycursor.execute('CREATE TABLE IF NOT EXISTS Surveys (id int AUTO_INCREMENT PRIMARY KEY, email varchar(255), title varchar(255) , description varchar(255), created_on DATE, expired_on Date, surveys_id int, visibility varchar(255))')
    mydb.commit()

    sql="Insert into Surveys (email, title, description, created_on, expired_on, surveys_id, visibility) values (%s,%s,%s,%s,%s,%s,%s)"
    email = "test@email.com"
    survey_title = "test title"
    survey_description = "test description"
    expired_date = None
    survey_id = 1
    visibility = 'public'

    val=(email, survey_title, survey_description, created_date, expired_date, survey_id, visibility)
    mycursor.execute(sql,val)
    mydb.commit()

    expected_outcome = [{'survey_id': 1, 'survey_title': 'test title', 'survey_description': 'test description'}]

    actual_outcome = retrievePublicSurveys()

    if str(expected_outcome) == actual_outcome:
        mycursor = mydb.cursor()
        sql = "DROP TABLE IF EXISTS Surveys"
        mycursor.execute(sql)
        mycursor.close()
        return "Passed!"
    else:
        mycursor = mydb.cursor()
        sql = "DROP TABLE IF EXISTS Surveys"
        mycursor.execute(sql)
        mycursor.close()
        return "Failed"





