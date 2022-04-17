import db_connector
def initial():
    mydb = db_connector.dbConnector()
    mycursor = mydb.cursor()

    sql = "create table if not exists Response (response_id int AUTO_INCREMENT PRIMARY KEY, question_id int, survey_id int,short_answer varchar(255), multiple_choice_answer varchar(255), email varchar(255))"
    mycursor.execute(sql)
    mydb.commit()
    # create table Surveys if not exists
    sql = "CREATE TABLE IF NOT EXISTS Surveys (id int AUTO_INCREMENT PRIMARY KEY, email varchar(255), title varchar(255), description varchar(255), created_on BIGINT, expired_on BIGINT, surveys_id int, visibility varchar(255), unique_url varchar(255), unique_string varchar(255), status varchar(255))"
    mycursor.execute(sql)
    mydb.commit()

    # create table Survey_Questions if not exists
    sql = "CREATE TABLE IF NOT EXISTS Survey_Questions (id int AUTO_INCREMENT PRIMARY KEY, question_id int, survey_id int)"
    mycursor.execute(sql)
    mydb.commit()

    # create table Questions if not exists
    sql = "CREATE TABLE IF NOT EXISTS Questions (id int AUTO_INCREMENT PRIMARY KEY, survey_id int, question_id int, question_title varchar(255), question_type varchar(255), options varchar(255))"
    mycursor.execute(sql)
    mydb.commit()

    # create table if not exists
    sql = "create table if not exists Users (id int AUTO_INCREMENT PRIMARY KEY, email varchar(255), password varchar(255), date_created DATE )"
    mycursor.execute(sql)
    mydb.commit()

    mydb.close()
    return

def drop():
    mydb = db_connector.dbConnector()
    mycursor = mydb.cursor()

    sql = "drop TABLE IF EXISTS Surveys"
    mycursor.execute(sql)
    mydb.commit()
    sql = "drop TABLE IF EXISTS Survey_Questions"
    mycursor.execute(sql)
    mydb.commit()
    sql = "drop TABLE IF EXISTS Questions"
    mycursor.execute(sql)
    mydb.commit()
    sql = "drop table if exists Users"
    mycursor.execute(sql)
    mydb.commit()
    sql = "drop table if exists Response"
    mycursor.execute(sql)
    mydb.commit()
    return