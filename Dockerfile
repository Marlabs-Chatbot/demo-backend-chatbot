FROM rasa/rasa-sdk:latest

WORKDIR /app

# Change back to root user to install dependencies
USER root

# # To install system dependencies
# RUN apt-get update -qq && \
#     apt-get install -y curl jq && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./actions /app/actions

# Switch back to non-root to run code
USER 1001

