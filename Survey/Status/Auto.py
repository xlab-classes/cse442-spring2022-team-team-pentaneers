import json

from flask import Flask

import db_connector
from datetime import datetime
from datetime import date

def autoClose():
    actualDate=datetime.now()
    actualDate=int(datetime.timestamp(actualDate))
    mydb = db_connector.dbConnector()
    mycursor = mydb.cursor(buffered=True)
    surveys_with_expiration_dates = "SELECT * FROM Surveys WHERE expired_on IS NOT NULL"
    mycursor.execute(surveys_with_expiration_dates)

    close_survey = "UPDATE Surveys SET status = %s, expired_on = null WHERE (expired_on IS NOT NULL AND expired_on <= %s)"
    val = ("close", actualDate)
    mycursor.execute(close_survey, val)
    mydb.commit()
    mydb.close()
    return True
'''
import datetime
import time
from apscheduler.schedulers.blocking import BackgroundScheduler
def job_function():

   print("Hello World" + " " + str(datetime.datetime.now()))


if __name__ == '__main__':
    print('start to do it')
    sched = BlockingScheduler()
    sched.add_job(job_function, 'cron', day_of_week='mon-fri', hour='13-19', minute="*", second="*/4") # 每4秒执行一次
    sched.start()
'''