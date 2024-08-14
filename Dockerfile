FROM python:3.9-slim

RUN apt-get update && apt-get install -y gettext

WORKDIR /app

COPY . /app

ARG TOKEN
ARG BOT_USERNAME
ARG GOOGLE_API_KEY
ARG YOUTUBE_API_KEY
ARG FROM_EMAIL
ARG FROM_PASSWORD
ARG TO_EMAIL

ENV TOKEN=${TOKEN} \
    BOT_USERNAME=${BOT_USERNAME} \
    GOOGLE_API_KEY=${GOOGLE_API_KEY} \
    YOUTUBE_API_KEY=${YOUTUBE_API_KEY} \
    FROM_EMAIL=${FROM_EMAIL} \
    FROM_PASSWORD=${FROM_PASSWORD} \
    TO_EMAIL=${TO_EMAIL}

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
    fi && \
    if [ -f locale/te/LC_MESSAGES/messages.po ]; then \
        msgfmt -o locale/te/LC_MESSAGES/messages.mo locale/te/LC_MESSAGES/messages.po; \
    else \
        echo "Warning: Telugu .po file not found"; \
    fi && \
    if [ -f locale/bn/LC_MESSAGES/messages.po ]; then \
        msgfmt -o locale/bn/LC_MESSAGES/messages.mo locale/bn/LC_MESSAGES/messages.po; \
    else \
        echo "Warning: Bengali .po file not found"; \
    fi && \
    if [ -f locale/zh_CN/LC_MESSAGES/messages.po ]; then \
        msgfmt -o locale/zh_CN/LC_MESSAGES/messages.mo locale/zh_CN/LC_MESSAGES/messages.po; \
    else \
        echo "Warning: Mandarin Chinese .po file not found"; \
    fi
    
EXPOSE 8080

CMD gunicorn app:app & python TelegramBot/quizly_telegram_bot.py