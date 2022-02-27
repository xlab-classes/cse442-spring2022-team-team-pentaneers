from flask import Flask
import mysql.connector
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


# Adding in UB's MYSQL Database (Make sure to change the formatting)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mahdyfer:50313245@oceanus.cse.buffalo.edu/cse442_2022_spring_team_ab_db'

# Initialize the database
Database = SQLAlchemy(app)


@app.route("/")
def test_database():
    Schema = ""
    mydb = mysql.connector.connect(
    host="oceanus.cse.buffalo.edu",
    user="mahdyfer",
    passwd = "50313245"
)

    db_cursor = mydb.cursor()

    db_cursor.execute("SHOW DATABASES")
    for db in db_cursor:
        Schema += str(db)
        Schema += "<br>"
    return "<p>Connected to UB's MYSQL database!</p>" + "<p>Here are the current Schema's:</p>" + Schema

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
