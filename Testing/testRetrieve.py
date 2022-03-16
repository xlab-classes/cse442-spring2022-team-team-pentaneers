import sys, os, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from Testing import testRetrievePublicSurveys, testRetrieveSurveyById, testRetrieveSurveyForResponse, testRetrieveSurveyResults, testRetrieveUserSurveys


def testAll():
    user_surveys = testRetrieveUserSurveys.test()
    public_surveys = testRetrievePublicSurveys.test()
    survey_by_id = testRetrieveSurveyById.test()
    survey_for_response = testRetrieveSurveyForResponse.test()
    survey_results = testRetrieveSurveyResults.test()
    return (user_surveys, public_surveys, survey_by_id, survey_for_response, survey_results)

results = testAll()
for result in results:
    print(result)