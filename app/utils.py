import pandas as pd
import calendar
import csv

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(user, password: str):
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def change_zero(val):
    val_c = val.split(' ')[0].split('-')
    my_str = val_c.copy()
    if my_str[1].startswith('0'):
        my_str[1] = my_str[1][1:]
    return my_str

def read_csv(file):
    with open(file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        rows = [row for row in csvreader]
    if len(rows) == 1 and rows[0] == ['Id', 'Date', 'Transaction']:
        first_number = 0
    else:
        data_row = rows[-1]
        first_number = int(data_row[0])
    return first_number
        

def extract_info_csv(file):

    df = pd.read_csv(file)
    #Calculate total balance
    total_balance = df['Transaction'].sum() 
    total_balance = round(total_balance,2) 

    #Number of Transactions per month
    number_transactions = [i.split('/')[0] for i in df['Date']]
    month_transactions = [calendar.month_name[int(i)] for i in number_transactions]
    df['Months'] = month_transactions #New column with month of transaction
    per_month = {val:cnt for val, cnt in df.Months.value_counts().items()}

    #Average credit amount per month
    credit_transactions = df[df['Transaction']>0]
    credit_transactions_avg_month = {val:cnt for val, cnt in 
                                     credit_transactions.groupby('Months')['Transaction'].mean().items()}

    #Average debit amount per month
    debit_transactions = df[df['Transaction']<0]
    debit_transactions_avg_month = {val:cnt for val, cnt in 
                                    debit_transactions.groupby('Months')['Transaction'].mean().items()}
    
    return total_balance, per_month, credit_transactions_avg_month, debit_transactions_avg_month


def send_bank_statement(total_balance, per_month,
                        credit_transactions_avg_month,
                        debit_transactions_avg_month,
                        user_name):
    
    sender_email = settings.SENDER_EMAIL
    sender_password = settings.SENDER_PASSWORD
    recipient_email = settings.RECIPIENT_EMAIL
    subject = 'Bank Montly Statement'

    statement_month = 'Here is your bank statement for the month of '
    
    month_names = [month for month in per_month.keys()]

    if len(month_names) == 1:
        months_str = month_names[0]
    else:
        last_month = month_names.pop()
        months_str = ", ".join(month_names) + " and " + last_month

    statement_month = f"Here is your bank statement for the month of {months_str}" + "for "

    statement_string_credit = "Your Average credit transactions per month: "
    for month, amount in credit_transactions_avg_month.items():
        statement_string_credit += f"{month}: ${amount}, "
    statement_string_credit = statement_string_credit[:-2] + "."

    statement_string_debit = "Your Average debit transactions per month: "
    for month, amount in debit_transactions_avg_month.items():
        statement_string_debit += f"{month}: ${amount}, "
    statement_string_debit = statement_string_debit[:-2] + "."

    body = '''
    Dear {},

    ''' + statement_month+'''

    Total balance: ${}
    ''' + statement_string_credit+'''
    ''' + statement_string_debit + '''
    Thank you for banking with us!

    Sincerely,
    Your Bank
    '''
    body = body.format(user_name,
                   total_balance,
                   debit_transactions_avg_month)
    # Set up the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(sender_email, sender_password)
        smtp.send_message(message)