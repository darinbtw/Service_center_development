from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, security
from .database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def read_root():
    return {'message': 'Сервер работает! Перейдите на /docs для документации.'}


@app.post('/auth/register', response_model=schemas.Token)
def register(user_data: schemas.UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.login == user_data.login).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователь с таким логином уже существует'
        )
    
    hashed_pw = security.get_password_hash(user_data.password)

    new_user = models.User(
        login=user_data.login,
        hashed_passwod=hashed_pw,
        fio=user_data.fio,
        phone_number=user_data.phone_number,
        role='Client'
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = security.create_access_token(
        data={'sub': new_user.login, 'role': new_user.role}
    )

    return {'access_token': access_token, 'token_type': 'bearer', 'role': new_user.role}

@app.post('/auth/login', response_model=schemas.Token)
def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.login == user_data.login).first()

    if not user or not security.verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный логин или пароль',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    
    access_token = security.create_access_token(
        data={'sub': user.login, 'role':user.role}
    )

    return {'access_token': access_token, 'token_type': 'bearer', 'role': user.role}
