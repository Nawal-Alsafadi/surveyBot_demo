import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from flask import render_template, request, redirect, url_for
from flask import  request, render_template, redirect, url_for

from api.routes.survey_bluePrint import survey_bp
summary_list =[]
class SurveyBotLogic :
    summ=[]
    def get_survey_by_id(self,survey_id):
        if survey_id == 1 :
            with open('api/survey.json', 'r') as file:
                survey_questions = json.load(file)
        if survey_id == 2 :
            with open('api/survey2.json', 'r') as file:
                survey_questions = json.load(file)
        if survey_id == 3 :
            with open('api/survey3.json', 'r') as file:
                survey_questions = json.load(file)
        return survey_questions    
    
    def get_survey_from_json(self,survey_path):
        with open('api/survey.json', 'r') as file:
            survey_questions = json.load(file)
        return survey_questions
    
    def determine_next_question_for_demo(self,user_input , survey_questions):
        current_question = user_input.get("current_question", "cold_start_message")



        if current_question in survey_questions:

            question_data = survey_questions[current_question]
            user_response = user_input.get(question_data.get("field", ""), "")

            if isinstance(user_response, list):
                user_response = [response.lower() for response in user_response]
            else:
              
                user_response = user_response.lower()

        
            


            if "yes_no" in question_data["type"]:
                next_question = question_data.get("next_question_yes" if user_response == "yes" else "next_question_no", "")


            elif "radio" in question_data["type"]:
                choices =[ x.lower() for x in  question_data.get("choices", [])]

                    
                nextQ = [ x.lower() for x in question_data.get("next_question", [])]
  
                next_question = nextQ[choices.index(user_response)]       

                
            else:
                next_question = question_data.get("next_question", "")
            
            self.summ.append((current_question, question_data.get("text", ""), user_response))
            print(self.summ)


            return next_question

        return "end_message"
    
    def determine_next_question(self,user_input , survey_questions,current_question):

        if current_question in survey_questions:
            
            question_data = survey_questions[current_question]
            user_response = user_input.get(question_data.get("field", ""), "")

            if isinstance(user_response, list):
                user_response = [response.lower() for response in user_response]
            else:

                user_response = user_response.lower()

        
            
 

            if "yes_no" in question_data["type"]:
                next_question = question_data.get("next_question_yes" if user_response == "yes" else "next_question_no", "")


            elif "radio" in question_data["type"]:
                choices =[ x.lower() for x in  question_data.get("choices", [])]

                    
                nextQ = [ x.lower() for x in question_data.get("next_question", [])]
             
                next_question = nextQ[choices.index(user_response)]       

                
            else:
                next_question = question_data.get("next_question", "")

            return next_question

        return "end_message"
