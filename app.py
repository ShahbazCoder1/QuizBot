from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
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

if __name__ == '__main__':
    # Run the Flask app on port 80
    app.run(host='0.0.0.0', port=8080)