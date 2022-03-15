import mysql.connector
def dbConnector(usr):
    return mysql.connector.connect(
        host="localhost",
        user=usr,
        password="",
        database = "testdb"
    )