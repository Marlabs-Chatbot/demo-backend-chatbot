FROM rasa/rasa-sdk:latest

WORKDIR /app


# Change back to root user to install dependencies
USER root

# COPY requirements.txt /app/requirements.txt
RUN pip install pymongo

COPY ./actions /app/actions

# Switch back to non-root to run code
USER 1001

