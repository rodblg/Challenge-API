from fastapi import FastAPI,Response,status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db
from .. import oauth2

import os

folder_path = 'static'

router = APIRouter()

@router.post('/transactions',status_code=status.HTTP_200_OK, response_model=schemas.TransactionReturn)
def new_transaction(item: schemas.Transaction, db : Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):

    new_transaction = models.Transaction(value=item.value, 
                                         name_movement=item.name_movement,user_id=current_user.id)
    
    new_value = float(current_user.balance) + float(item.value)
    current_user.balance = new_value

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    user = db.query(models.User).filter(models.User.email==current_user.email).first()

    file_name = str(user.email).split('@')[0] + str(user.created_at).split(' ')[0] + '.csv'
    file_path = os.path.join(folder_path,file_name)

    val_date = str(user.created_at)
    #print(type(val_date), val_date)
    val_date_c = utils.change_zero(val_date)
    f_date = val_date_c[1] + '/' + val_date_c[2]
    id = utils.read_csv(file_path)

    rows = [{'Id': str(id+1), 'Date': f_date, 'Transaction': str(item.value)}]

    with open(file_path, 'a') as f:
        for row in rows:
            f.write(f"{row['Id']},{row['Date']},{row['Transaction']}\n")
    
    return new_transaction 

@router.get('/transactions',status_code=status.HTTP_200_OK)
def bank_statement(db : Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    
    user = db.query(models.User).filter(models.User.email==current_user.email).first()

    file_name = str(user.email).split('@')[0] + str(user.created_at).split(' ')[0] + '.csv'
    file_path = os.path.join(folder_path,file_name)

    total_balance, per_month, credit_transactions_avg_month, debit_transactions_avg_month = utils.extract_info_csv(file_path)

    utils.send_bank_statement(total_balance, per_month, credit_transactions_avg_month,
                               debit_transactions_avg_month,user.name)
    return {'message': 'Bank Statement sent to the user'}