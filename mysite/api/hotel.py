from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import Hotel, Country, UserProfile, City, Service
from db.schema import HotelCreateSchema, HotelListSchema, HotelDetailSchema
from typing import List

hotel_router = APIRouter(prefix='/hotel', tags=['Hotel'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@hotel_router.post('/create', response_model=HotelCreateSchema)
async def create_hotel(hotel_data: HotelCreateSchema, db: Session = Depends(get_db)):
    hotel_country = db.query(Country).filter(Country.id == hotel_data.country_id)
    if not hotel_country:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такой страны нет!')
    hotel_city = db.query(City).filter(City.id == hotel_data.city_id).first()
    if not hotel_city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого города нет!')
    hotel_service = db.query(Service).filter(Service.id == hotel_data.service_id).first()
    if not hotel_service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого сервиса нет!')
    hotel_owner = db.query(UserProfile).filter(UserProfile.id == hotel_data.owner_id).first()
    if not hotel_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого пользователя нет!')
    hotel_db = Hotel(**hotel_data.dict())
    db.add(hotel_db)
    db.commit()
    db.refresh(hotel_db)
    return hotel_db

@hotel_router.get('/list', response_model=List[HotelListSchema])
async def list_hotel(db: Session = Depends(get_db)):
    hotel_db = db.query(Hotel).all()
    return hotel_db

@hotel_router.get('/detail/{hotel_id}', response_model=HotelDetailSchema)
async def detail_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel_db = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого жилья нет!')
    return hotel_db

@hotel_router.put('/update/{hotel_id}', response_model=dict)
async def update_hotel(hotel_id: int, hotel_data: HotelCreateSchema, db: Session = Depends(get_db)):
    hotel_db = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого жилья нет!')
    for key, value in hotel_data.dict().items():
        setattr(hotel_db, key, value)
    db.commit()
    db.refresh(hotel_db)
    return {'status': 'Успешно изменено!'}

@hotel_router.delete('/delete/{hotel_id}', response_model=dict)
async def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel_db = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого жилья нет!')
    db.delete(hotel_db)
    db.commit()
    return {'status': 'Успешно удалено!'}