from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import UserProfile
from db.schema import UserProfileUpdateSchema, UserProfileListSchema, UserProfileDetailSchema
from typing import List

user_router = APIRouter(prefix='/user', tags=['UserProfile'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user_router.get('/list', response_model=List[UserProfileListSchema])
async def list_user(db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).all()
    return user_db

@user_router.get('/detail/{user_id}', response_model=UserProfileDetailSchema)
async def detail_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого пользователя нет!')
    return user_db

@user_router.put('/update/{user_id}', response_model=dict)
async def update_user(user_id: int, user_data: UserProfileUpdateSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого пользователя нет!')
    for key, value in user_data.dict().items():
        setattr(user_db, key, value)
    db.commit()
    db.refresh(user_db)
    return {'status': 'Успешно изменено!'}

@user_router.delete('/delete/{user_id}', response_model=dict)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого пользователя нет!')
    db.delete(user_db)
    db.commit()
    return {'status': 'Успешно удалено!'}