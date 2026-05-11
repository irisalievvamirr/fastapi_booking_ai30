from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import Service
from db.schema import ServiceCreateSchema, ServiceListSchema
from typing import List

service_router = APIRouter(prefix='/service', tags=['Service'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@service_router.post('/create', response_model=ServiceCreateSchema)
async def create_service(service_data: ServiceCreateSchema, db: Session = Depends(get_db)):
    service_db = Service(service_name=service_data.service_name, service_image=service_data.service_image)
    db.add(service_db)
    db.commit()
    db.refresh(service_db)
    return service_db

@service_router.get('/list', response_model=List[ServiceListSchema])
async def list_service(db: Session = Depends(get_db)):
    service_db = db.query(Service).all()
    return service_db

@service_router.get('/detail/{service_id}', response_model=ServiceListSchema)
async def detail_service(service_id: int, db: Session = Depends(get_db)):
    service_db = db.query(Service).filter(Service.id == service_id).first()
    if not service_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого сервиса нет!')
    return service_db

@service_router.put('/update/{service_id}', response_model=dict)
async def update_service(service_id: int, service_data: ServiceCreateSchema, db: Session = Depends(get_db)):
    service_db = db.query(Service).filter(Service.id == service_id).first()
    if not service_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого сервиса нет!')
    for key, value in service_data.dict().items():
        setattr(service_db, key, value)
    db.commit()
    db.refresh(service_db)
    return {'status': 'Успешно изменено!'}

@service_router.delete('/delete/{service_id}', response_model=dict)
async def delete_service(service_id: int, db: Session = Depends(get_db)):
    service_db = db.query(Service).filter(Service.id == service_id).first()
    if not service_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого сервиса нет!')
    db.delete(service_db)
    db.commit()
    return {'status': 'Успешно удалено!'}