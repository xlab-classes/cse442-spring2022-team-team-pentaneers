import json

from Survey.Retrieve import parseSurveyQuestions, RetrieveSurveyById
import db_connector
import datetime

from Survey.Status import Auto
from db_initial import drop


def openSurvey(surveys_id,email):
    ''' data: {"expires_date": Date or Null}'''
    # when reopen a survey, expires_on may be NULL
    mydb = db_connector.dbConnector()
    mycursor = mydb.cursor()
    close_survey = "UPDATE Surveys SET visibility = %s WHERE surveys_id = %s and email=%s"
    val = ("public", surveys_id,email)
    mycursor.execute(close_survey, val)
    mydb.commit()
    return True