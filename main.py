import google.generativeai as genai
from tqdm import tqdm
import time

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

# Program Start here:
GOOGLE_API_KEY='AIzaSyC_1F8N1oLYOXvv_MJ21Yp0GlRU6ksT2R4'

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
            response = model.generate_content(f"Generate a python dictionary which contains 10 {level} level questions on {topic} from {sub} along with four options as possible answers for each question. Show the four options along with alphabets assigned to them serially. Return only the dictonary code part.")
            pbar.update(50) #progress bar update by 50/100
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            pbar.update(100)
            time.sleep(0.5) 

incor = 0
cor = 0

quiz = response.text.replace("```","").replace("python","")

print(eval(quiz))

'''
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
    print("Selected topic is not available.") '''

print(f"\nNumber of correct answers: {cor}")
print(f"Number of incorrect answers: {incor}")  
if cor==10:
    print("Excellent performance🥳!")
elif cor>7:
    print("Great performance😃!")
elif cor>5:
    print("Good job! Just a little more push🥰")
else:
    print("Keep working. Better luck next time :)")