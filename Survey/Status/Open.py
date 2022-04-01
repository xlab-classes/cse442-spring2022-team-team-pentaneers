import json

from Survey.Retrieve import parseSurveyQuestions, RetrieveSurveyById
import db_connector
import datetime

def openSurvey(id,data):
    ''' data: {"expires_date": Date or Null}'''
    # when reopen a survey, expires_on may be NULL
    data=json.loads(data)
    expired = data['expired_date']
    if(expired==None):
        mydb = db_connector.dbConnector()
        mycursor = mydb.cursor()
        close_survey = "UPDATE Surveys SET visibility = %s, expires_on = null WHERE id = %s"
        val = ("private", id)
        mycursor.execute(close_survey, val)
        mydb.commit()
    else:
        expired = datetime.datetime.strptime(expired, "%Y-%m-%d").date()
        mydb = db_connector.dbConnector()
        mycursor = mydb.cursor()
        close_survey = "UPDATE Surveys SET visibility = %s, expired_on = %s WHERE id = %s"
        val = ("private", expired, id)
        mycursor.execute(close_survey, val)
        mydb.commit()

    # for test
    query="SELECT * FROM Surveys WHERE id = %s"
    value = (id,)
    mycursor.execute(query, value)
    # Fetch the survey information belonging to the requested Survey
    survey = mycursor.fetchall()
    survey = survey[0]
    mydb.close()
    return json.dumps(survey)