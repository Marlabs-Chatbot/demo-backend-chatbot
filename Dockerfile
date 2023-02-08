FROM rasa/rasa:3.4.1-full

WORKDIR /app

# COPY requirements.txt /app/requirements.txt
# RUN pip install pymongo

COPY ./data /app/data
COPY ./models /app/models
COPY ./config.yml /app/config.yml
COPY ./domain.yml /app/domain.yml
COPY ./endpoints.yml /app/endpoints.yml
COPY ./credentials.yml /app/credentials.yml
COPY ./Dockerfile /app/Dockerfile
