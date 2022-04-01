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
    val = ("private", id)
    mycursor.execute(close_survey, val)
    mydb.commit()
    query = "SELECT * FROM Surveys WHERE id = %s"
    value = (id,)
    mycursor.execute(query, value)
    # Fetch the survey information belonging to the requested Survey
    survey = mycursor.fetchall()
    survey = survey[0]
    mydb.close()
    return json.dumps(survey)
