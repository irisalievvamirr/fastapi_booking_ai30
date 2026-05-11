from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import ImageRoom, Room
from db.schema import ImageRoomCreateSchema, ImageRoomListSchema
from typing import List

image_room_router = APIRouter(prefix='/image_room', tags=['ImageRoom'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@image_room_router.post('/create', response_model=ImageRoomCreateSchema)
async def create_image_room(ir_data: ImageRoomCreateSchema, db: Session = Depends(get_db)):
    image_room_id = db.query(Room).filter(Room.id == ir_data.room_id).first()
    if not image_room_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  detail='Такой комнаты нет!')
    ir_db = ImageRoom(**ir_data.dict())
    db.add(ir_db)
    db.commit()
    db.refresh(ir_db)
    return ir_db

@image_room_router.get('/list', response_model=List[ImageRoomListSchema])
async def list_image_room(db: Session = Depends(get_db)):
    ir_db = db.query(ImageRoom).all()
    return ir_db

@image_room_router.get('/detail/{image_room_id', response_model=ImageRoomListSchema)
async def detail_image_room(image_room_id: int, db: Session = Depends(get_db)):
    ir_db = db.query(ImageRoom).filter(ImageRoom.id == image_room_id).first()
    if not ir_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого изображения нет!')
    return ir_db

@image_room_router.put('/update/{image_room_id}', response_model=dict)
async def update_image_room(image_room_id: int, ir_data: ImageRoomCreateSchema, db: Session = Depends(get_db)):
    ir_db = db.query(ImageRoom).filter(ImageRoom.id == image_room_id).first()
    if not ir_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого изображения нет!')
    for key, value in ir_data.dict().items():
        setattr(ir_db, key, value)
    db.commit()
    db.refresh(ir_db)
    return {'status': 'Успешно изменено!'}

@image_room_router.delete('/delete/{image_room_id}', response_model=dict)
async def delete_image_room(image_room_id: int, db: Session = Depends(get_db)):
    ir_db = db.query(ImageRoom).filter(ImageRoom.id == image_room_id).first()
    if not ir_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого изображения нет!')
    db.delete(ir_db)
    db.commit()
    return {'status': 'Успешно удалено!'}