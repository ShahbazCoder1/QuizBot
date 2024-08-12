FROM python:3.9-slim

RUN apt-get update && apt-get install -y gettext

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install python-telegram-bot --upgrade

RUN if [ -f locale/en/LC_MESSAGES/messages.po ]; then \
        msgfmt -o locale/en/LC_MESSAGES/messages.mo locale/en/LC_MESSAGES/messages.po; \
    else \
        echo "Warning: English .po file not found"; \
    fi && \
    if [ -f locale/es/LC_MESSAGES/messages.po ]; then \
        msgfmt -o locale/es/LC_MESSAGES/messages.mo locale/es/LC_MESSAGES/messages.po; \
    else \
        echo "Warning: Spanish .po file not found"; \
    fi && \
    if [ -f locale/hi/LC_MESSAGES/messages.po ]; then \
        msgfmt -o locale/hi/LC_MESSAGES/messages.mo locale/hi/LC_MESSAGES/messages.po; \
    else \
        echo "Warning: Hindi .po file not found"; \
    fi

ENV TOKEN = TOKEN
ENV USERNAME = USERNAME
ENV API_KEY = API_KEY
ENV YOUTUBE_API = YOUTUBE_API
ENV SEND_EMAIL = SEND_EMAIL
ENV PASSWORD = PASSWORD
ENV RECEIVER_EMAIL = RECEIVER_EMAIL

EXPOSE 8080

# Command to run the Flask application
CMD ["python", "main.py"]