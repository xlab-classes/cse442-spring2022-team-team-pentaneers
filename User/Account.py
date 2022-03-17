import datetime
import json
import db_connector
from datetime import date
from db_initial import initial

def account(data):
    email = data['email']
    password = data['password']
    created_date = date.today()

    # connect database
    mydb = db_connector.dbConnector()
    mycursor = mydb.cursor()

    # create tables if not exist
    initial()

    # check account is created or not
    sql = "select * from Users where email=%s"
    val = (email,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    if (len(myresult) != 0): return json.dumps("account exists")

    # insert user information
    sql = "Insert into Users (email, password, date_created) values (%s,%s,%s)"
    val = (email, password, created_date)
    mycursor.execute(sql, val)
    mydb.commit()

    # select user_id
    sql = "select id from Users where email=%s"
    val = (email,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    returnid = 0
    
    for result in myresult:
        returnid += int(str(result[0]))

    mydb.close()
    return json.dumps(returnid)