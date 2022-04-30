import db_connector
from Survey.Status import Auto


def retrieveSurveyResults(email, surveys_id):
    Auto.autoClose()
    final_list = []

    # Access the Database
    mydb = db_connector.dbConnector()
    mycursor = mydb.cursor()
    # Access the Surveys table to get the specific Survey for the user.
    query = "SELECT * FROM Surveys WHERE email = %s AND surveys_id = %s"
    values = (email, surveys_id)
    mycursor.execute(query, values)
    result = mycursor.fetchall()

    survey_id = result[0][0]

    query = "SELECT * FROM Questions WHERE survey_id = %s"
    value = (survey_id, )
    # Execute our MySQL Query to get what we want
    mycursor.execute(query, value)
    # Fetch all Questions belonging to the requested Survey
    survey_questions = mycursor.fetchall()
    print("These are the survey questions: ", survey_questions)

    # Check survey exists
    if len(result) == 0:
        return "survey not exists"

    # Getting the title of the survey
    survey_title = result[0][2]
    survey_id = result[0][0]

    query = "SELECT * FROM Response WHERE survey_id = %s"
    values = (survey_id, )
    mycursor.execute(query, values)
    # fetch all the matching rows 
    result = mycursor.fetchall()
    print("This is the retrieve results: ", result)

    list_to_return = []


    short_responses_array = []
    sr_question_names = []
    sr_question_responses = []
    
    multiple_choices_array = []
    mc_question_names = []
    mc_question_options = []
    mc_question_responses = []

    for question_number in range(0, len(survey_questions)):
        question_name = survey_questions[question_number][3]
        question_type = survey_questions[question_number][4]
        question_options = survey_questions[question_number][5]
        #------------------------------------------------------#
        if question_type == 'Multiple Choice':
            mc_options = []
            mc_question_names.append(question_name)
            parsed_options = getOptions(question_options)
            if len(parsed_options) != 0:
              for option in parsed_options:
                  mc_options.append(option)
              mc_question_options.append(mc_options)
              question_responses = countOptions(result, question_number, len(mc_options))
              mc_question_responses.append(question_responses)
        #-----------------------------------------------------#
        if question_type == 'Short Response':
            sr_question_names.append(question_name)
            question_responses = shortAnswerResponses(result, question_number)
            sr_question_responses.append(question_responses)

    total_number_of_responders = 0
    for response in result:
      question_number = response[1]
      if question_number == 1:
        total_number_of_responders += 1



    multiple_choices_array.append(mc_question_names)
    multiple_choices_array.append(mc_question_options)
    multiple_choices_array.append(mc_question_responses)
    list_to_return.append(multiple_choices_array)

    short_responses_array.append(sr_question_names)
    short_responses_array.append(sr_question_responses)
    list_to_return.append(short_responses_array)
    list_to_return.append(total_number_of_responders)

    return list_to_return




def getOptions(mc_options):
  parsed_options = []
  split_options = mc_options.split(';')
  split_options.remove('')
  for curr_option in split_options:
    option_start = curr_option.find(':')+1
    parsed_options.append(curr_option[option_start:len(curr_option)])
  return parsed_options


def shortAnswerResponses(respones, question_number):
  complete_responses = []
  for responses in respones:
    curr_question_number = responses[1]
    short_response_answer = responses[3]
    email = responses[5]
    if curr_question_number == question_number+1:
      full_response = email + ' wrote: ' + short_response_answer
      complete_responses.append(full_response)
  return complete_responses


def countOptions(results, question_number, number_of_options):
    final_list = [0] * number_of_options
    for result in results:
        if result[1] == question_number+1:
            int_option = int(result[4])-1
            final_list[int_option] = final_list[int_option] + 1
    return final_list