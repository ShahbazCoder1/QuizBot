'''
Title: Run Telegram Bot using Flask
Code Written by: 𝗠𝗱 𝗦𝗵𝗮𝗵𝗯𝗮𝘇 𝗛𝗮𝘀𝗵𝗺𝗶 𝗔𝗻𝘀𝗮𝗿𝗶
programing languages: Python
Description: The code utilizes Flask, a web framework, to execute the quizly_telegram_bot.py script. This is used to ease the 
deployment of the code in form of a web application.
Code Version: V1.0
Copyright ©: Open-source
'''

from flask import Flask, render_template
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    return "Running!"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()