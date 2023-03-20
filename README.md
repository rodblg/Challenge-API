# Challenge-API

# FastAPI API Bank App
This project implements a FastAPI API that imitates how a bank app would work. It allows you to create a new account for an user, log in with those credentials, make transactions, and then send a report by email with the average of movements for the month.

## Features
- Register and Login with email/password, JWT authentication
- Make a registry of credit and debit transactions in your account that will be saved in a PostgreSQL db
- Send a report by email with the average of movements for the month
- Contenized 

## Technologies Used
- FastAPI
- SQLAlchemy
- Alembic
- Docker
- Python

## Installation and Configuration Instructions without the Docker image
1. Clone the repository
2. Create a virtual environment: `py -m venv venv`
3. Install the requirements: `pip install -r requirements.txt`
4. Start the application: `uvicorn app.main:app`

## Installation and Configuration Instructions with the Docker image
This project has been pushed to the Docker Hub as an image. To access and run the image locally, complete the following steps: 
1. Pull the image from the Docker Hub: `docker pull roblancas/challenge-api`
2. Run the image with the docker-compose command: `docker-compose -f docker-compose-prod.yml up -d`
3. Access the API on http://localhost:5005