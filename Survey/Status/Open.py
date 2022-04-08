import json

from Survey.Retrieve import parseSurveyQuestions, RetrieveSurveyById
import db_connector
import datetime

def openSurvey(id,data):
    ''' data: {"expires_date": Date or Null}'''
    # when reopen a survey, expires_on may be NULL
    expired = data['expired_date']
    if(expired==None):
        mydb = db_connector.dbConnector()
        mycursor = mydb.cursor()
        close_survey = "UPDATE Surveys SET visibility = %s, expires_on = null WHERE id = %s"
        val = ("public", id)
        mycursor.execute(close_survey, val)
        mydb.commit()
    else:
        expired = datetime.datetime.strptime(expired, "%Y-%m-%d").date()
        mydb = db_connector.dbConnector()
        mycursor = mydb.cursor()
        close_survey = "UPDATE Surveys SET visibility = %s, expired_on = %s WHERE id = %s"
        val = ("public", expired, id)
        mycursor.execute(close_survey, val)
        mydb.commit()
    return True