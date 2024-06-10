import google.generativeai as genai
import os

# Main method
title = '''
  ____        _ 
 / __ \      (_) 
| |  | |_   _ _ ____ 
| |  | | | | | |_  / 
| |__| | |_| | |/ /_
 \___\_\\__,__|_/____|
 ____        _   
|  _ \      | |  
| |_) | ___ | |_ 
|  _ < / _ \| __|
| |_) | (_) | |_ 
|____/ \___/ \__|
'''
print(title)

GOOGLE_API_KEY='AIzaSyC_1F8N1oLYOXvv_MJ21Yp0GlRU6ksT2R4'

genai.configure(api_key=GOOGLE_API_KEY) #apikey configuration

model = genai.GenerativeModel('gemini-1.5-flash') #model setup

topic = input("Enter the topic you wish to take a quiz on: ").upper()

response = model.generate_content("Generate a python dictionary which contains 10 questions on "+ topic + "along with four options and among those 4 options one answer should be the correct option.") 
incor = 0
cor = 0

print(response.text)



'''
print("\nLIST OF TOPICS AVAILABLE\n1.JAVA\n2.PYTHON\n3.MYSQL\n")
topic = input("Enter the topic you wish to take a quiz on: ").upper()
incor = 0
cor = 0

# dictionary
dic = {
    "JAVA": [
        {
            "question": "What is the default value of a boolean variable in java?\n a. true\n b. 0\n c. false\n d. void",
            "answer": "c"
        },
        {
            "question": "Which of the following is not a primitive data type in Java?\n a. int\n b. char\n c. String\n d. None of the above",
            "answer": "c"
        },
        {
            "question": "Which method is called when an object is created in Java?\n a. constructor\n b. finalize()\n c. main()\n d. int()",
            "answer": "a"
        },
        {
            "question": "What is the size of an int variable in Java?\n a. 4 bytes\n b. char\n c. String\n d. None of the above",
            "answer": "a"
        }
    ],
    "PYTHON": [
        {
            "question": "What is the output of print(2 ** 3)?\n a. 5\n b. 8\n c. 6\n d. 9",
            "answer": "b"
        },
        {
            "question": "Which of the following is a mutable data type in Python?\n a. tuple\n b. int\n c. list\n d. str",
            "answer": "c"
        },
        {
            "question": "How do you start a comment in Python?\n a. //\n b. <!--\n c. /*\n d. #",
            "answer": "d"
        },
        {
            "question": "What does the len() function do?\n a. Returns the number of items in an object\n b. Converts a value to an integer\n c. Returns a list of numbers\n d. Creates an empty dictionary",
            "answer": "a"
        }
    ],
    "MYSQL": [
        {
            "question": "What does SQL stand for?\n\na. Structured Query Language\nb. Simple Query Language\nc. Structured Question Language\nd. None of the above",
            "answer": "a"
        },
        {
            "question": "Which SQL keyword is used to sort the result set?\na. ORDER \nb. ORDER BY\nc. SORT BY\nd. None of the above",
            "answer": "b"
        },
        {
            "question": "Which SQL keyword is used to filter the result set? \na. FILTER BY\nb. FILTER\nc. WHERE\nd. None of the above",
            "answer": "c"
        },
        {
            "question": "How do you select all the columns from a table named 'employees'?\na. SELECT EMPLOYEES;\nb. SELECT * from employees\nc. SELECT all from employees\nd. None of the above",
            "answer": "b"
        }
    ]
}


if topic in dic:
    for i in dic[topic]:
        x = input("\n"+ "Q: " + i["question"] + "\n" + "\nAnswer: ").lower()
        if x == i["answer"].lower():
            print("\nCorrect")
            cor += 1
        else:
            print("\nIncorrect")
            incor += 1
else:
    print("Selected topic is not available.")

print(f"\nNumber of correct answers: {cor}")
print(f"Number of incorrect answers: {incor}")  '''