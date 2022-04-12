import unittest
import sys, os, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
parent_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(1, parent_parent_dir)

from db_initial import initial,drop
import db_connector
from Survey.Create.Survey import survey
from Survey.Retrieve.RetrieveSurveyForResponseByString import retrieve

class MyTestCase(unittest.TestCase):

    def testGenerateURL(self):
        drop()
        Survey = {"email": "test@email.com","title": "test1","description":"test description 1","questions":[['do you like cats?', 'Multiple Choice', ['yes', 'no']],['why', 'Short Response', None],['do you wanna keep coding?', 'Multiple Choice', ['pain', 'wuyu']]],"expired_date": "2022-03-22","visibility":"public"}
        survey(Survey)

        # connect database
        mydb = db_connector.dbConnector()
        mycursor = mydb.cursor()

        # create tables if they don't exist
        initial()

        # Get all of the surveys from the 'Surveys' table.
        query = "SELECT * FROM Surveys"
        # Execute our MySQL Query to get what we want
        mycursor.execute(query)
        # fetch all the matching rows 
        result = mycursor.fetchall()

        email = result[0][1]
        survey_title = result[0][2]
        url = result[0][8]
        unique_string = result[0][9]

        # Retrieve the survey by the unique string
        retrieved = retrieve(1, unique_string)
        print(retrieved)
        self.assertGreater(len(result), 0)
        self.assertEqual(email, "test@email.com")
        self.assertEqual(survey_title, "test1")
        self.assertNotEqual(url, None)
        self.assertGreater(len(retrieved), 0)
        self.assertEqual(retrieved[0], survey_title)
        
        

if __name__ == '__main__':
    unittest.main()