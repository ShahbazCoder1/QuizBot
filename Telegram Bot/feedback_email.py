'''
Title: Feedback email with smtplib
Code Written by: 𝗠𝗱 𝗦𝗵𝗮𝗵𝗯𝗮𝘇 𝗛𝗮𝘀𝗵𝗺𝗶 𝗔𝗻𝘀𝗮𝗿𝗶
programing languages: Python
Code Version: V1.0
Copyright ©: Open-source
'''

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pytz
import os

def send_feedback_email(feedback_data):
    from_email = os.getenv('send_email')
    from_password = os.getenv('password')
    to_email = os.getenv('receiver_email')
    utc_date = feedback_data['date']
    ist_timezone = pytz.timezone('Asia/Kolkata')
    ist_date = utc_date.astimezone(ist_timezone)

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "New Feedback for Quizly Bot"

    body = f"""
    <html>
    <body>
        <p>Hi There,</p>
        <p>Quizly has a new feedback:</p>
        <blockquote>{feedback_data['feedback_text']}</blockquote>
        <p><strong>Sender Details:</strong></p>
        <ul>
            <li><strong>Name:</strong> {feedback_data['name']}</li>
            <li><strong>User ID:</strong> {feedback_data['chat_id']}</li>
            <li><strong>Chat Type:</strong> {feedback_data['chat_type']}</li>
            <li><strong>Date & Time:</strong> {ist_date.strftime("%Y-%m-%d %H:%M:%S")} (IST)</li>
            <li><strong>Is Bot:</strong> {feedback_data['is_bot']}</li>
        </ul>
    </body>
    </html>
    """

    msg.attach(MIMEText(body, 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)