from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import List
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os


load_dotenv()


app = FastAPI()


SECRET_KEY = os.getenv("SECRET_KEY") 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 86400


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=84000))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")