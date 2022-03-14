def parseSurveyQuestions(question):
    parsed_questions = []

    for question in question:
        List = []
        choice_list = []
        question_title = question[3]
        question_type = question[4]
        choice = question[5]
        List.append(question_title)
        List.append(question_type)
        if choice != None:
            choices = choice.split(";")
            choices.remove('')
            for choice in choices:
                start_choice = choice.find(":") + 1
                choice = choice[start_choice:]
                choice_list.append(choice)
            List.append(choice_list)
        else:
            List.append(None)

        parsed_questions.append(List)
        
    return str(parsed_questions)