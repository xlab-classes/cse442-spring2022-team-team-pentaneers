import json

from Survey.Retrieve import parseSurveyQuestions, RetrieveSurveyById
import db_connector
import datetime

from Survey.Status import Auto


def closeSurvey(surveys_id,email):
    # param id is primary key of Survey Table
    # when close a survey, set expires_on NULL
    mydb = db_connector.dbConnector()
    mycursor = mydb.cursor()
    close_survey = "UPDATE Surveys SET visibility = %s, expired_on = null WHERE surveys_id = %s and email=%s"
    val = ("private", surveys_id,email)
    mycursor.execute(close_survey, val)
    mydb.commit()
    mydb.close()
    Auto.autoClose()
    return True