# Base image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Accept build arguments
ARG OKTA_ISSUER
ARG OKTA_AUDIENCE
ARG FLASK_ENV

# Set environment variables
ENV OKTA_ISSUER=$OKTA_ISSUER
ENV OKTA_AUDIENCE=$OKTA_AUDIENCE
ENV FLASK_ENV=$FLASK_ENV

# Install dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app code
COPY app/ .

# Expose Flask port
EXPOSE 5001

# Default command
CMD ["python", "main.py"]
