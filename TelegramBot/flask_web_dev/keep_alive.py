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
  return """
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Telegram Bot Status</title>
      <style>
          body {
              font-family: Arial, sans-serif;
              background-color: #f4f4f4;
              color: #333;
              display: flex;
              justify-content: center;
              align-items: center;
              height: 100vh;
              margin: 0;
          }
          .container {
              text-align: center;
              background: white;
              padding: 20px;
              border-radius: 10px;
              box-shadow: 0 0 10px rgba(0,0,0,0.1);
          }
          h1 {
              color: #007bff;
          }
          p {
              margin: 20px 0;
          }
          a {
              color: #007bff;
              text-decoration: none;
              font-weight: bold;
          }
          a:hover {
              text-decoration: underline;
          }
      </style>
  </head>
  <body>
      <div class="container">
          <h1>Bot is Running!</h1>
          <p>You can now start chatting with the bot.</p>
          <p><a href="https://t.me/Quisly_Bot" target="_blank">Open Telegram Bot</a></p>
      </div>
  </body>
  </html>
  """

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()