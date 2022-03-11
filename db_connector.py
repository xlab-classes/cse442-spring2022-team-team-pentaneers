import mysql.connector
def dbConnector(usr,pwd):
    return mysql.connector.connect(
        host="localhost",
        user=usr,
        password=pwd,
        database = "testdb"
    )