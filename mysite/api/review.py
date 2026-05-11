from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import Review, UserProfile, Hotel
from db.schema import ReviewCreateSchema, ReviewListSchema
from typing import List

review_router = APIRouter(prefix='/review', tags=['Review'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@review_router.post('/create', response_model=ReviewCreateSchema)
async def create_review(review_data: ReviewCreateSchema, db: Session = Depends(get_db)):
    review_user = db.query(UserProfile).filter(UserProfile.id == review_data.user_id).first()
    if not review_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого пользователя нет!')
    review_hotel = db.query(Hotel).filter(Hotel.id == review_data.hotel_id).first()
    if not review_hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого жилья нет!')
    review_db = Review(**review_data.dict())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db

@review_router.get('/list', response_model=List[ReviewListSchema])
async def list_review(db: Session = Depends(get_db)):
    review_db = db.query(Review).all()
    return review_db

@review_router.get('/detail/{review_id}', response_model=ReviewListSchema)
async def detail_review(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого отзыва нет!')
    return review_db

@review_router.put('/update/{review_id}', response_model=dict)
async def update_review(review_id: int, review_data: ReviewCreateSchema, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого отзыва нет!')
    for key, value in review_data.dict().items():
        setattr(review_db, key, value)
    db.commit()
    db.refresh(review_db)
    return {'status': 'Успешно изменено!'}

@review_router.delete('/delete/{review_id}', response_model=dict)
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого отзыва нет!')
    db.delete(review_db)
    db.commit()
    return {'status': 'Успешно удалено!'}

