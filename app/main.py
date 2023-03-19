#This script will help you to read a csv file and to send an email with the extracted info

from fastapi import FastAPI
from .routers import user,auth,transactions


app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(transactions.router)


@app.get("/")
def root():
    return {"message": "Hello World it works!!!"}

