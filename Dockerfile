FROM rasa/rasa:3.1.0

WORKDIR /app


# Change back to root user to install dependencies
USER root

# COPY requirements.txt /app/requirements.txt
# RUN pip install pymongo

COPY ./data /app/data
COPY ./models /app/models
COPY ./config.yml /app/config.yml
COPY ./domain.yml /app/domain.yml
COPY ./endpoints.yml /app/endpoints.yml
COPY ./Dockerfile /app/Dockerfile

# Switch back to non-root to run code
USER 1001