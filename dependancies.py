from urllib import request

from fastapi import Depends, HTTPException, Request, status
from flask import request
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import EmailStr
from fastapi.templating import Jinja2Templates

SECRET_KEY = "change_this_secret_for_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
templates = Jinja2Templates(directory="templates")

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

        is_admin = False

        if email == "admin@gmail.com":
            is_admin = True

        return {
            "email": email,
            "is_admin": is_admin
        }

    except JWTError:
        raise credentials_exception
    
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates 
from database import get_db
from sqlalchemy.orm import Session

def create_employees(email: str, name:str , is_admin : int, db: Session):
    from model_db import User
    user = User(username=email, email=email, name=name, is_admin=is_admin)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_employees(employee_id: int, db: Session):
    from model_db import User
    user = db.query(User).filter(User.id == employee_id).first()
    error = HTTPException(status_code=404, detail="User not found")
    if user:
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    else:
        raise error
        
def update_employees(employee_id: int, email: EmailStr, name: str, is_admin: int, db: Session):
    from model_db import User
    user = db.query(User).filter(User.id == employee_id).first()
    error = HTTPException(status_code=404, detail="User not found")
    if user:
        user.name = name
        user.email = email
        user.is_admin = is_admin
        db.commit()
        db.refresh(user)
        return user
    else:
        raise error