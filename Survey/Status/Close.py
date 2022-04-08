import json

from Survey.Retrieve import parseSurveyQuestions, RetrieveSurveyById
import db_connector
import datetime

def closeSurvey(id):
    # param id is primary key of Survey Table
    # when close a survey, set expires_on NULL
    mydb = db_connector.dbConnector()
    mycursor = mydb.cursor()
    close_survey = "UPDATE Surveys SET visibility = %s, expired_on = null WHERE id = %s"
    val = ("close", id)
    mycursor.execute(close_survey, val)
    mydb.commit()
    mydb.close()
    return True
