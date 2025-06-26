# 🧪 Project 01 – IAM Flask Microservice (Docker + CI)

A starter microservice to simulate identity API health, built with Flask, containerized using Docker, and deployed via GitHub Actions.

## 🚀 Features

- Health check endpoint: `/health`
- Dockerized app
- GitHub Actions pipeline: auto-build on commit

## 🧱 Run Locally

```bash
docker build -t iam-demo .
docker run -p 5000:5000 iam-demo
