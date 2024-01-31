import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from flask import jsonify, render_template, request, redirect, url_for
from flask import  request, render_template, redirect, url_for

from api.routes.survey_bluePrint import survey_bp
from api.MyApp.survey.surveyBotLogic import SurveyBotLogic
survey_data = {
    "name": "",
    "age": "",
    "email": "",
    "course": "",
    "problems_in_course": "",
    "join_another_course": "",
    "courses_to_join": "",
    "comment": "",
    "numeric":"",
    "overall_rating": "",
}
summary_list=[]
with open('api/survey.json', 'r') as file:
    survey_questions_from_file = json.load(file)
    
survey_questions = survey_questions_from_file

all_responses = []

@survey_bp.route('/')
def home():
    return render_template('index.html')
my_bot_logic = SurveyBotLogic()
@survey_bp.route('/surveydemo', methods=['POST'])
def surveydemo():
    
    
    user_input = request.form.to_dict(flat=False)
    for key, value in user_input.items():
        if isinstance(value, list) and len(value) == 1:
            user_input[key] = value[0]
    survey_data.update(user_input)

    
    next_question = my_bot_logic.determine_next_question_for_demo(user_input, survey_questions)
    
    if next_question == "end_message":
        print("summ",my_bot_logic.summ)
        summary_list = my_bot_logic.summ[:]
        print("summary_list",summary_list)
        all_responses.append(survey_data.copy())
        summary_list.append(my_bot_logic.summ.copy())
        
        return redirect(url_for('surveydemo.summary'))
    else:    return render_template('survey.html', question=survey_questions[next_question], question_id=next_question, message=survey_data.get('cold_start_message', ''), user_input=user_input)

@survey_bp.route('/summary', methods=['GET'])
def summary():
    summary_list = my_bot_logic.summ[:]
    print("opo",summary_list)
    return render_template('summary.html', summary_list=summary_list)



from flask import jsonify

@survey_bp.route('/survey', methods=['GET', 'POST'])
def survey():
    my_bot_logic = SurveyBotLogic()

    if request.method == 'GET':
        # Serve the start question to the frontend
        start_question = my_bot_logic.determine_next_question(survey_data, survey_questions,"cold_start_message")
        start_question_data = survey_questions.get(start_question, {})
        
        response = {
            "question_id": start_question,
            "question_text": start_question_data.get("text", ""),
            "question_type": start_question_data.get("type", ""),
            "question_choices": start_question_data.get("choices", []),
            "question_fields": start_question_data.get("fields", [])
        }
        return jsonify(response)

    elif request.method == 'POST':
        # Receive user answer and store it
        user_input = request.form.to_dict(flat=False)
        current_question_id =str(user_input.get("current_question", [""])[0])  # Retrieve the current question ID
        
        for key, value in user_input.items():
            if isinstance(value, list) and len(value) == 1:
                user_input[key] = str(value[0])

        survey_data.update(user_input)
        next_question = my_bot_logic.determine_next_question(user_input, survey_questions,current_question_id)

        next_question_data = survey_questions.get(next_question, {})
        response = {
            "question_id": next_question,
            "question_text": next_question_data.get("text", ""),
            "question_type": next_question_data.get("type", ""),
            "question_choices": next_question_data.get("choices", [])
        }
        return jsonify(response)