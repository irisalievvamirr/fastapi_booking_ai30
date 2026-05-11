from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import UserProfile, RefreshToken
from datetime import timezone, timedelta, datetime
from db.schema import RegisterSchema, LoginSchema
from passlib.context import CryptContext
from config import SECRET_KEY, ACCESS_EXPIRE_TOKEN, REFRESH_EXPIRE_TOKEN, ALGORITHM
import jwt

auth_router = APIRouter(prefix='/auth', tags=['Authorization'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password):
    return password_context.hash(password)

def verify_password(password, hashed_password):
    return password_context.verify(password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_EXPIRE_TOKEN)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    return create_access_token(data=data, expires_delta=timedelta(days=REFRESH_EXPIRE_TOKEN))

@auth_router.post('/register', response_model=dict)
async def register(register_data: RegisterSchema, db: Session = Depends(get_db)):
    user_db_username = db.query(UserProfile).filter(UserProfile.username == register_data.username).first()
    user_db_email = db.query(UserProfile).filter(UserProfile.email == register_data.email).first()
    if user_db_username or user_db_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Такой username или email уже есть!')
    hashed_password = hash_password(register_data.password)
    register_db = UserProfile(
        username=register_data.username,
        first_name=register_data.first_name,
        last_name=register_data.last_name,
        phone_number=register_data.phone_number,
        email=register_data.email,
        password=hashed_password
    )
    db.add(register_db)
    db.commit()
    db.refresh(register_db)
    return {'status': 'Успешно создан аккаунт!'}

@auth_router.post('/login', response_model=dict)
async def login(login_data: LoginSchema, db: Session = Depends(get_db)):
    login_db = db.query(UserProfile).filter(UserProfile.username == login_data.username).first()
    login_db_password = verify_password(login_data.password, login_db.password)
    if not login_db or not login_db_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Пароль или Имя пользователя неверны!')

    access_token = create_access_token({'sub': login_db.username})
    refresh_token = create_refresh_token({'sub': login_db.username})
    refresh_token_db = RefreshToken(user_id=login_db.id, token=refresh_token)

    db.add(refresh_token_db)
    db.commit()
    db.refresh(refresh_token_db)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'type': 'Bearer',
        'user': login_db.username,
        'email': login_db.email
    }

@auth_router.post('/generate_access_token', response_model=dict)
async def generate_access_token(refresh_token: str, db: Session = Depends(get_db)):
    refresh_db = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not refresh_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого refresh token нет!')
    access_token = create_access_token({'sub': refresh_db.user_id})
    return {
        'access_token': access_token,
        'type': 'Bearer'
    }

@auth_router.post('/logout', response_model=dict)
async def logout(refresh_token: str, db: Session = Depends(get_db)):
    refresh_db = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not refresh_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого refresh token нет!')
    db.delete(refresh_db)
    db.commit()
    return {'status': 'Вы успешно вышли с аккаунта!'}