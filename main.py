'''
Title: Quiz Bot
Code Written by: 𝗠𝗱 𝗦𝗵𝗮𝗵𝗯𝗮𝘇 𝗛𝗮𝘀𝗵𝗺𝗶 𝗔𝗻𝘀𝗮𝗿𝗶, 𝗩𝗶𝗱𝗵𝗶 𝗔𝗴𝗿𝗮𝘄𝗮𝗹
programing languages: Python
Description: This code is a quiz bot that generates a quiz based on the user's chosen subject, topic, and difficulty level 
using the Google Generative AI API, presents the questions to the user, and provides feedback on their performance. A simple
Console based game with 10 questions. 𝐓𝐡𝐢𝐬 𝐜𝐨𝐝𝐞 𝐢𝐬 𝐟𝐮𝐫𝐭𝐡𝐞𝐫 𝐦𝐨𝐝𝐢𝐟𝐢𝐞𝐝 𝐢𝐧𝐭𝐨 𝐚 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐁𝐨𝐭 '𝐐𝐮𝐢𝐳𝐥𝐲'.
Code Version: V1.0
Copyright ©: Open-source
'''

import google.generativeai as genai
from tqdm import tqdm
import time
import os

# Main method
print( '''
  ____          _ 
 / __ \        (_) 
| |  | | _   _  _  ____ 
| |  | || | | || ||_  / 
| |__| || |_| || | / /_ 
 \___\_\ \__,_||_|/____|
 ____          _   
|  _ \        | |  
| |_) |  ___  | |_ 
|  _ <  / _ \ | __|
| |_) || (_) || |_ 
|____/  \___/  \__|
''' )

#intructions here:
print("Welcome to Quiz Bot. Get ready to challenge your knowledge with our exciting quiz. Choose the subject, topic and difficulty level according to your convenience and answer the questions that follows.\n")

# Program Start here:
GOOGLE_API_KEY=os.getenv('API_KEY')

genai.configure(api_key=GOOGLE_API_KEY) #apikey configuration

model = genai.GenerativeModel('gemini-1.5-flash') #model setup
# User input
sub=input("Enter the subject you wish to take the quiz on: ").upper()
topic = input("Enter the topic you wish to take a quiz on: ").upper()
level= input("Enter the level of the quiz [beginner/intermediate/advanced]: ").upper()
# Start the progress bar
print("\nGenerating quiz questions, please wait...")
with tqdm(total=100, desc="Generating", ncols=100) as pbar:
    response = None
    while response is None:
        pbar.update(20) #progress bar update by 20/100
        try:
            # Response here
            response = model.generate_content(f"""Generate a python dictionary which contains 10 {level} level questions on {topic} from {sub} along with four options as possible answers for each question. Show the four options along with alphabets assigned to them serially. Return only the dictionary code part.

            The dictionary should have the following structure:

            The main dictionary contains 10 key-value pairs, with keys 'Q1' through 'Q10'.
            Each question is represented by a nested dictionary containing three key-value pairs:
            1. 'question': A string containing the question text.
            2. 'options': A nested dictionary with keys 'A', 'B', 'C', and 'D', each corresponding to a possible answer.
            3. 'answer': A string containing the letter of the correct answer ('A', 'B', 'C', or 'D').

            Example structure for one question:

            {{
                'Q1': {{
                        'question': 'What is the question text?',
                        'options': {{
                            'A': 'First option',
                            'B': 'Second option',
                            'C': 'Third option',
                            'D': 'Fourth option'
                    }},
                'answer': 'C'
                }}
            }}

            Ensure that all questions are related to the specified topic and subject, and match the specified difficulty level. Return only the Python dictionary code, without any additional text or explanations.""")
            pbar.update(50) #progress bar update by 50/100
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            pbar.update(100)
            time.sleep(0.5) 

incor = 0
cor = 0

quiz = eval(response.text.replace("```","").replace("python",""))

for key, value in quiz.items():
    print(f"\nQ: {value['question']}")
    options = value['options']
    for opt_key, opt_value in options.items():
        print(f"{opt_key}: {opt_value}")

    x = input("Enter your answer (a-d): ").strip().lower()

    if x == value['answer']:
        cor += 1
        print("Correct")
    else:
        incor += 1
        print("Incorrect")

print(f"\nNumber of correct answers: {cor}")
print(f"Number of incorrect answers: {incor} \n")  
if cor==10:
    print("Excellent performance🥳!")
elif cor>7:
    print("Great performance😃!")
elif cor>5:
    print("Good job! Just a little more push🥰")
else:
    print("Keep working. Better luck next time :)")