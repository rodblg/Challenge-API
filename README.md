# Challenge-API

# FastAPI API Bank App
This project implements a FastAPI API that imitates how a bank app would work. It allows you to create a new account for an user, log in with those credentials, make transactions, and then send a report by email with the average of movements for the month.

## Features
- Register and Login with email/password, JWT authentication
- Make a registry of credit and debit transactions in your account that will be saved in a PostgreSQL db
- Send a report by email with the average of movements for the month
- Containerized with Docker

## Technologies Used
- FastAPI
- SQLAlchemy
- Alembic
- Docker
- Python

## Installation and Configuration Instructions without the Docker image
1. Clone the repository
2. Create a virtual environment: `py -m venv venv`
3. Activate the virtual environment: `venv\Scripts\activate.bat`
4. Install the requirements: `pip install -r requirements.txt`
5. Start the application: `uvicorn app.main:app`
6. Access the API with this endpoint structure: `http://127.0.0.1:8000/{path_operation}`
7. You can send the Requests with Postman

## Installation and Configuration Instructions with the Docker image
This project has been pushed to the Docker Hub as an image. To access and run the image locally, complete the following steps: 
1. Pull the image from the Docker Hub: `docker pull roblancas/challenge-api`
2. Update your credentials in the `environments/production.env` file. For more information about the environment variables check the `credentials_example.env` file
3. Run the image with the docker-compose command: `docker-compose -f docker-compose-prod.yml up -d`
4. Access the API with this endpoint structure: `http://127.0.0.1:8000/{path_operation}`
5. You can send the Requests with Postman

## Path Operations
This project has 3 endpoints to handle the necessary operations: 
- /users: This endpoint allows you to create new user accounts and manage existing user accounts. Requires a JSON object as input. The format for the object is as follows: 
``` 
{ 
    "name": "<name>", 
    "email": "<email>", 
    "password": "<password>" 
} 
``` 
- /login: This endpoint allows you to log into an existing account with a username and password.
The endpoint for logging into an existing account requires two form-data parameters: 
1. Email: This is the email address associated with the account. 
2. Password: This is the password associated with the account.  
3. It's important to save the Token retrived after the user login, it will be required to create transactions, and to view user info.

- /transactions: This endpoint allows you to make transactions between user accounts. 
The endpoint for making transactions requires a JSON object as input. The format for the object is as follows: 
``` 
{ 
    "value": <value>, 
    "name_movement": "<name_movement>" 
} 
``` 
Where <value> is the amount to be transferred, and "<name_movement>" is the label or name associated with the transaction.

## Postman configuration
You can use the postman collection to make new requests into the API following this steps:
1. Download the json file into your local machine.
2. Import it into your workspace.
3. To use the collection you have to create a postman environment and define the variable URL as your localhost `http://127.0.0.1:8000`in case it is not defined.
