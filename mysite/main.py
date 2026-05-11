from fastapi import FastAPI
from api import user, country, city, service, hotel, image_hotel, room, image_room, review, booking_hotel, auth
from admin.setup import setup_admin

booking_app = FastAPI(title='FastAPI Booking AI30')
booking_app.include_router(user.user_router)
booking_app.include_router(country.country_router)
booking_app.include_router(city.city_router)
booking_app.include_router(service.service_router)
booking_app.include_router(hotel.hotel_router)
booking_app.include_router(image_hotel.image_hotel_router)
booking_app.include_router(room.room_router)
booking_app.include_router(image_room.image_room_router)
booking_app.include_router(review.review_router)
booking_app.include_router(booking_hotel.booking_hotel_router)
booking_app.include_router(auth.auth_router)

setup_admin(booking_app)