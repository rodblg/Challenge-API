from fastapi import FastAPI,Response,status, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, utils, oauth2,schemas
from app.database import get_db

router = APIRouter()

@router.post("/login", status_code=status.HTTP_200_OK,response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')
    
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {'access_token': access_token, "token_type": "bearer"}



