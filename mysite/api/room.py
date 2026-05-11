from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import Room, Hotel
from db.schema import RoomCreateSchema, RoomListSchema
from typing import List

room_router = APIRouter(prefix='/room', tags=['Room'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@room_router.post('/create', response_model=RoomCreateSchema)
async def create_room(room_data: RoomCreateSchema, db: Session = Depends(get_db)):
    room_hotel = db.query(Hotel).filter(Hotel.id == room_data.hotel_id)
    if not room_hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого жилья нет!')
    room_db = Room(**room_data.dict())
    db.add(room_db)
    db.commit()
    db.refresh(room_db)
    return room_db

@room_router.get('/list', response_model=List[RoomListSchema])
async def list_room(db: Session = Depends(get_db)):
    room_db = db.query(Room).all()
    return room_db

@room_router.get('/detail/{room_id}', response_model=RoomListSchema)
async def detail_room(room_id: int, db: Session = Depends(get_db)):
    room_db = db.query(Room).filter(Room.id == room_id).first()
    if not room_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такой комнаты нет!')
    return room_db

@room_router.put('/update/{room_id}', response_model=dict)
async def update_room(room_id: int, room_data: RoomCreateSchema, db: Session = Depends(get_db)):
    room_db = db.query(Room).filter(Room.id == room_id).first()
    if not room_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такой комнаты нет!')
    for key, value in room_data.dict().items():
        setattr(room_db, key, value)
    db.commit()
    db.refresh(room_db)
    return {'status': 'Успешно изменено!'}

@room_router.delete('/delete/{room_id}', response_model=dict)
async def delete_room(room_id: int, db: Session = Depends(get_db)):
    room_db = db.query(Room).filter(Room.id == room_id).first()
    if not room_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такой комнаты нет!')
    db.delete(room_db)
    db.commit()
    return {'status': 'Успешно удалено!'}

