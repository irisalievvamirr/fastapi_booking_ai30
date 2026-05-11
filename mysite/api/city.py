from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import City, Country
from db.schema import CityCreateSchema, CityListSchema
from typing import List

city_router = APIRouter(prefix='/city', tags=['City'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@city_router.post('/create', response_model=CityCreateSchema)
async def create_city(city_data: CityCreateSchema, db: Session = Depends(get_db)):
    city_country_id = db.query(Country).filter(Country.id == city_data.country_id).first()
    if not city_country_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такой страны нет!')
    city_db = City(country_id=city_data.country_id, city_name=city_data.city_name)
    db.add(city_db)
    db.commit()
    db.refresh(city_db)
    return city_db

@city_router.get('/list', response_model=List[CityListSchema])
async def list_city(db: Session = Depends(get_db)):
    city_db = db.query(City).all()
    return city_db

@city_router.get('/detail/{city_id}', response_model=CityListSchema)
async def detail_city(city_id: int, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого города нет!')
    return city_db

@city_router.put('/update/{city_id}', response_model=dict)
async def update_city(city_id: int, city_data: CityCreateSchema, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого города нет!')
    for key, value in city_data.dict().items():
        setattr(city_db, key, value)
    db.commit()
    db.refresh(city_db)
    return {'status': 'Успешно изменено'}

@city_router.delete('/delete/{city_id}', response_model=dict)
async def delete_city(city_id: int, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого города нет!')
    db.delete(city_db)
    db.commit()
    return {'status': 'Успешно удалено'}