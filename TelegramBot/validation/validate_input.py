'''
Title:  Subject and Topic Input Validation using Gemini
Code Written by: 𝗠𝗱 𝗦𝗵𝗮𝗵𝗯𝗮𝘇 𝗛𝗮𝘀𝗵𝗺𝗶 𝗔𝗻𝘀𝗮𝗿𝗶
programing languages: Python
Description: This code utilizes the Gemini language model to validate if a given subject and topic are 
valid academic entities by generating text-based responses and converting them to boolean values.
Copyright ©: Open-source
'''

import google.generativeai as genai
import os

genai.configure(api_key=os.getenv('API_KEY'))
model = genai.GenerativeModel('gemini-1.0-pro')

#convert string to bool
def str_to_bool(s):
    if s.lower() in ['true', '1', 't', 'y', 'yes']:
        return True
    elif s.lower() in ['false', '0', 'f', 'n', 'no']:
        return False
    else:
        raise ValueError(f"Cannot cast {s} to a boolean.")

#validate Subject
async def validate_subject(subject):
    prompt = f"Is \"{subject}\" a valid academic subject or field of study? Please respond with only 'True' or 'False'."
    response = model.generate_content(prompt)
    #print(response.text)
    return str_to_bool(response.text)

#validate if topic is from that subject only
async def validate_topic(subject, topic):
    prompt = f"Is \"{topic}\" a valid topic within the subject of \"{subject}\"? Please respond with only 'True' or 'False'."
    response = model.generate_content(prompt)
    #print(response.text)
    return str_to_bool(response.text)