from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class RegisterSchema(BaseModel):
    first_name: str | None
    last_name: str | None
    username: str
    phone_number: str
    email: EmailStr
    password: str

class LoginSchema(BaseModel):
    username: str
    password: str

class UserProfileUpdateSchema(BaseModel):
    first_name: str | None
    last_name: Optional[str]
    username: str
    age: int | None
    phone_number: str | None
    profile_image: Optional[str]
    email: EmailStr
    password: str

class UserProfileListSchema(BaseModel):
    id: int
    username: str
    phone_number: str
    profile_image: Optional[str]

class UserProfileDetailSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    age: int | None
    phone_number: str
    profile_image: Optional[str]

class CountryCreateSchema(BaseModel):
    country_name: str
    country_image: str

class CountryListSchema(BaseModel):
    id: int
    country_name: str
    country_image: str

class CityCreateSchema(BaseModel):
    country_id: int
    city_name: str

class CityListSchema(BaseModel):
    id: int
    country_id: int
    city_name: str

class ServiceCreateSchema(BaseModel):
    service_name: str
    service_image: str

class ServiceListSchema(BaseModel):
    id: int
    service_name: str
    service_image: str

class HotelCreateSchema(BaseModel):
    country_id: int
    city_id: int
    hotel_name: str
    hotel_image: str
    address: str
    service_id: int
    owner_id: int
    description: str | None


class HotelListSchema(BaseModel):
    id: int
    hotel_name: str
    hotel_image: str
    country_id: int
    city_id: int

class HotelDetailSchema(BaseModel):
    id: int
    country_id: int
    city_id: int
    hotel_name: str
    hotel_image: str
    address: str
    service_id: int
    owner_id: int
    description: str | None

class ImageHotelCreateSchema(BaseModel):
    hotel_id: int
    image: str

class ImageHotelListSchema(BaseModel):
    id: int
    hotel_id: int
    image: str

class RoomCreateSchema(BaseModel):
    hotel_id: int
    room_name: str
    room_image: str
    price: int

class RoomListSchema(BaseModel):
    id: int
    hotel_id: int
    room_name: str
    room_image: str
    price: int

class ImageRoomCreateSchema(BaseModel):
    room_id: int
    image: str

class ImageRoomListSchema(BaseModel):
    id: int
    room_id: int
    image: str

class ReviewCreateSchema(BaseModel):
    user_id: int
    hotel_id: int
    comment: str | None
    stars: int | None

class ReviewListSchema(BaseModel):
    id: int
    user_id: int
    hotel_id: int
    comment: str | None
    stars: int | None

class BookingHotelCreateSchema(BaseModel):
    user_id: int
    hotel_id: int
    room_id: int
    check_in_date: date
    check_out_date: date
    grown_ups: int
    children: int

class BookingHotelListSchema(BaseModel):
    id: int
    user_id: int
    hotel_id: int
    room_id: int
    check_in_date: date
    check_out_date: date
    grown_ups: int
    children: int