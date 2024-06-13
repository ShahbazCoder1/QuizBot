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
            response = model.generate_content(f"Generate a python dictionary which contains 10 {level} level questions on {topic} from {sub} along with four options as possible answers for each question. Show the four options with option numbers assigned to them serially and display the option number along with the answer while displaying the correct answer. Return only the dictonary code part.")
            pbar.update(50) #progress bar update by 50/100
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            pbar.update(100)
            time.sleep(0.5) 

incor = 0
cor = 0

quiz = eval(response.text.replace("```","").replace("python",""))

print(quiz)


for key, i in quiz.items():
    options_str = i.get('options')
    options_list = options_str  
    options_display = "\n".join([f"{j+1}. {option}" for j, option in enumerate(options_list)]) 
    x = input("\n" + f"Q: {key[1:]}: {i.get('question')}" + "\n" + options_display + "\nEnter your answer (1-4): ")


print(f"\nNumber of correct answers: {cor}")
print(f"Number of incorrect answers: {incor}")  
if cor==10:
    print("Excellent performance!")
elif cor>7:
    print("Great performance!")
elif cor>5:
    print("Good job! Just a little more push.")
else:
    print("You can do better!")