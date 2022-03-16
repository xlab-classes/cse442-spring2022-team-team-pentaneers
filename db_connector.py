import mysql.connector
import config

def dbConnector():
    return mysql.connector.connect(
        host = config.DATABASE_HOST,
        user = config.DATABASE_USER,
        password= config.DATABASE_PASSWORD,
        database = config.DATABASE_SCHEMA
    )