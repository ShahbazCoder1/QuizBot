FROM python:3.8
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install python-telegram-bot --upgrade
EXPOSE 8080
ENV API_KEY=$API_KEY
CMD ["python", "main.py"]

