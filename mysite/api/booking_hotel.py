from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import BookingHotel, UserProfile, Hotel, Room
from db.schema import BookingHotelCreateSchema, BookingHotelListSchema
from typing import List

booking_hotel_router = APIRouter(prefix='/booking_hotel', tags=['BookingHotel'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@booking_hotel_router.post('/create', response_model=BookingHotelCreateSchema)
async def create_booking_hotel(bh_data: BookingHotelCreateSchema, db: Session = Depends(get_db)):
    bh_user = db.query(UserProfile).filter(UserProfile.id == bh_data.user_id).first()
    if not bh_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого пользователя нет!')
    bh_hotel = db.query(Hotel).filter(Hotel.id == bh_data.hotel_id).first()
    if not bh_hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого жилья нет!')
    bh_room = db.query(Room).filter(Room.id == bh_data.room_id).first()
    if not bh_room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такой комнаты нет!')
    bh_db = BookingHotel(**bh_data.dict())
    db.add(bh_db)
    db.commit()
    db.refresh(bh_db)
    return bh_db

@booking_hotel_router.get('/list', response_model=List[BookingHotelListSchema])
async def list_booking_hotel(db: Session = Depends(get_db)):
    bh_db = db.query(BookingHotel).all()
    return bh_db

@booking_hotel_router.get('/detail/{booking_hotel_id}', response_model=BookingHotelListSchema)
async def detail_booking_hotel(booking_hotel_id: int, db: Session = Depends(get_db)):
    bh_db = db.query(BookingHotel).filter(BookingHotel.id == booking_hotel_id).first()
    if not bh_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такой брони нет!')
    return bh_db

@booking_hotel_router.put('/update/{booking_hotel_id}', response_model=dict)
async def update_booking_hotel(booking_hotel_id: int, bh_data: BookingHotelCreateSchema, db: Session = Depends(get_db)):
    bh_db = db.query(BookingHotel).filter(BookingHotel.id == booking_hotel_id).first()
    if not bh_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такой брони нет!')
    for key, value in bh_data.dict().items():
        setattr(bh_db, key, value)
    db.commit()
    db.refresh(bh_db)
    return {'status': 'Успешно изменено!'}

@booking_hotel_router.delete('/delete/{booking_hotel_id}', response_model=dict)
async def delete_booking_hotel(booking_hotel_id: int, db: Session = Depends(get_db)):
    bh_db = db.query(BookingHotel).filter(BookingHotel.id == booking_hotel_id).first()
    if not bh_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такой брони нет!')
    db.delete(bh_db)
    db.commit()
    return {'status': 'Успешно удалено!'}