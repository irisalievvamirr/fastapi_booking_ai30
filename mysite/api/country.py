from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import Country
from db.schema import CountryCreateSchema, CountryListSchema
from typing import List

country_router = APIRouter(prefix='/country', tags=['Country'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@country_router.post('/create', response_model=CountryCreateSchema)
async def create_country(country_data: CountryCreateSchema, db: Session = Depends(get_db)):
    country_db = Country(country_name=country_data.country_name, country_image=country_data.country_image)
    db.add(country_db)
    db.commit()
    db.refresh(country_db)
    return country_db

@country_router.get('/list', response_model=List[CountryListSchema])
async def list_country(db: Session = Depends(get_db)):
    country_db = db.query(Country).all()
    return country_db

@country_router.get('/detail/{country_id}', response_model=CountryListSchema)
async def detail_country(country_id: int, db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id == country_id).first()
    if not country_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такой страны нет!')
    return country_db

@country_router.put('/update/{country_id}', response_model=dict)
async def update_country(country_id: int, country_data: CountryCreateSchema, db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id == country_id).first()
    if not country_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такой страны нет!')
    for key, value in country_data.dict().items():
        setattr(country_db, key, value)
    db.commit()
    db.refresh(country_db)
    return {'status': 'Успешно изменено!'}

@country_router.delete('/delete/{country_id}', response_model=dict)
async def delete_country(country_id: int, db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id == country_id).first()
    if not country_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такой страны нет!')
    db.delete(country_db)
    db.commit()
    return {'status': 'Успешно удалено!'}