from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import ImageHotel, Hotel
from db.schema import ImageHotelCreateSchema, ImageHotelListSchema
from typing import List

image_hotel_router = APIRouter(prefix='/image_hotel', tags=['ImageHotel'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@image_hotel_router.post('/create', response_model=ImageHotelCreateSchema)
async def create_image_hotel(ih_data: ImageHotelCreateSchema, db: Session = Depends(get_db)):
    image_hotel_id = db.query(Hotel).filter(Hotel.id == ih_data.hotel_id).first()
    if not image_hotel_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого жилья нет!')
    ih_db = ImageHotel(**ih_data.dict())
    db.add(ih_db)
    db.commit()
    db.refresh(ih_db)
    return ih_db

@image_hotel_router.get('/list', response_model=List[ImageHotelListSchema])
async def list_image_hotel(db: Session = Depends(get_db)):
    ih_db = db.query(ImageHotel).all()
    return ih_db

@image_hotel_router.get('/detail/{image_hotel_id}', response_model=ImageHotelListSchema)
async def detail_image_hotel(image_hotel_id: int, db: Session = Depends(get_db)):
    ih_db = db.query(ImageHotel).filter(ImageHotel.id == image_hotel_id).first()
    if not ih_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого изображения нет!')
    return ih_db

@image_hotel_router.put('/update/{image_hotel_id}', response_model=dict)
async def update_image_hotel(image_hotel_id: int, ih_data: ImageHotelCreateSchema, db: Session = Depends(get_db)):
    ih_db = db.query(ImageHotel).filter(ImageHotel.id == image_hotel_id).first()
    if not ih_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого изображения нет!')
    for key, value in ih_data.dict().items():
        setattr(ih_db, key, value)
    db.commit()
    db.refresh(ih_db)
    return {'status': 'Успешно изменено!'}

@image_hotel_router.delete('/delete/{image_hotel_id}', response_model=dict)
async def delete_image_hotel(image_hotel_id: int, db: Session = Depends(get_db)):
    ih_db = db.query(ImageHotel).filter(ImageHotel.id == image_hotel_id).first()
    if not ih_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого изображения нет!')
    db.delete(ih_db)
    db.commit()
    return {'status': 'Успешно удалено!'}