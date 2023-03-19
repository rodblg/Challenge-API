from fastapi import FastAPI,Response,status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from ..utils import get_password_hash
import pandas as pd
import os

router = APIRouter()

folder_path = 'static'

#Path Operation to know logged user account information 
@router.get("/users",status_code=status.HTTP_200_OK, response_model=schemas.UserReturn)
def get_info_user(db: Session = Depends(get_db),  
                  current_user: int = Depends(oauth2.get_current_user)):
    
    user = db.query(models.User).filter(models.User.id==current_user.id).first()

    return user

#Create a new user account
@router.post("/users",status_code=status.HTTP_201_CREATED, response_model=schemas.UserReturn)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    created_user = db.query(models.User).filter(models.User.email==user.email).first()

    df = pd.DataFrame({}, columns=['Id', 'Date', 'Transaction'])
    file_name = str(created_user.email).split('@')[0] + str(created_user.created_at).split(' ')[0] + '.csv'

    if not os.path.exists(folder_path): os.mkdir(folder_path)

    file_path = os.path.join(folder_path,file_name)
    print('[LOG]: ',file_path)
    df.to_csv(file_path, index=False, header=True)
    
    return db_user 
