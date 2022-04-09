import json

from Survey.Retrieve import parseSurveyQuestions, RetrieveSurveyById
import db_connector
import datetime

from db_initial import drop


def openSurvey(surveys_id,data,email):
    ''' data: {"expires_date": Date or Null}'''
    # when reopen a survey, expires_on may be NULL
    expired = data['expired_date']
    if(expired==""):
        mydb = db_connector.dbConnector()
        mycursor = mydb.cursor()
        close_survey = "UPDATE Surveys SET visibility = %s, expired_on = null WHERE surveys_id = %s and email=%s"
        val = ("public", surveys_id,email)
        mycursor.execute(close_survey, val)
        mydb.commit()
    else:
        expired = datetime.datetime.strptime(expired, "%Y-%m-%d").date()
        mydb = db_connector.dbConnector()
        mycursor = mydb.cursor()
        close_survey = "UPDATE Surveys SET visibility = %s, expired_on = %s WHERE surveys_id = %s and email=%s"
        val = ("public", expired, surveys_id,email)
        mycursor.execute(close_survey, val)
        mydb.commit()
    return True