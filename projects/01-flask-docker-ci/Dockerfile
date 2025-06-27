FROM python:3.11-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

#Add .env file handling
COPY .env /app/.env

EXPOSE 5000
CMD ["python", "main.py"]
