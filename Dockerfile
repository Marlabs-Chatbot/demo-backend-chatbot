FROM python:3.9-slim

RUN python -m pip install rasa==3.1.0
RUN pip install pymongo

WORKDIR /app

COPY . /app
