FROM rasa/rasa-sdk:latest

WORKDIR /app


# Change back to root user to install dependencies
USER root

RUN pip install --no-cache-dir -r requirements.txt

COPY ./actions /app/actions

# Switch back to non-root to run code
USER 1001

