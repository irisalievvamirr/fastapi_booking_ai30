from .database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, SmallInteger, Enum, ForeignKey, Text, Date
from enum import Enum as PyEnum
from typing import Optional, List
from datetime import date

class UserRole(str, PyEnum):
    client = 'client'
    owner = 'owner'

class RoomType(str, PyEnum):
    family = 'family'
    single = 'single'
    double = 'double'
    luxury = 'luxury'

class RoomStatus(str, PyEnum):
    free = 'free'
    booked = 'booked'

class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    username: Mapped[str] = mapped_column(String(32), unique=True)
    email: Mapped[str] = mapped_column(String(32), unique=True)
    age: Mapped[int | None] = mapped_column(SmallInteger, default=0, nullable=True)
    phone_number: Mapped[str] = mapped_column(String, default='+996')
    profile_image: Mapped[str | None] = mapped_column(String, nullable=True)
    date_register: Mapped[date] = mapped_column(Date, default=date.today())
    user_role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.client)
    password: Mapped[str] = mapped_column(String)

    hotel_owner: Mapped[List['Hotel']] = relationship('Hotel', back_populates='owner', cascade='all, delete-orphan')
    user_review: Mapped[List['Review']] = relationship('Review', back_populates='user', cascade='all, delete-orphan')
    user_booking: Mapped[List['BookingHotel']] = relationship('BookingHotel', back_populates='user', cascade='all, delete-orphan')
    refresh_owner: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user', cascade='all, delete-orphan')

class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    token: Mapped[str] = mapped_column(String)

    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='refresh_owner')

class Country(Base):
    __tablename__ = 'country'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    country_name: Mapped[str] = mapped_column(String(32), unique=True)
    country_image: Mapped[str] = mapped_column(String)

    city_country: Mapped[List['City']] = relationship('City', back_populates='country', cascade='all, delete-orphan')
    country_hotel: Mapped[List['Hotel']] = relationship('Hotel', back_populates='country', cascade='all, delete-orphan')

    def __repr__(self):
        return self.country_name

class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    country_id: Mapped[int] = mapped_column(ForeignKey('country.id'))
    city_name: Mapped[str] = mapped_column(String(32))

    country: Mapped['Country'] = relationship('Country', back_populates='city_country')

    city_hotel: Mapped[List['Hotel']] = relationship('Hotel', back_populates='city', cascade='all, delete-orphan')

    def __repr__(self):
        return self.city_name

class Service(Base):
    __tablename__ = 'service'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    service_name: Mapped[str] = mapped_column(String(32))
    service_image: Mapped[str] = mapped_column(String)

    service_hotel: Mapped[List['Hotel']] = relationship('Hotel', back_populates='service', cascade='all, delete-orphan')

    def __repr__(self):
        return self.service_name

class Hotel(Base):
    __tablename__ = 'hotel'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    country_id: Mapped[int] = mapped_column(ForeignKey('country.id'))
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    hotel_name: Mapped[str] = mapped_column(String(32))
    hotel_image: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String(60))
    service_id: Mapped[int] = mapped_column(ForeignKey('service.id'))
    owner_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    country: Mapped['Country'] = relationship('Country', back_populates='country_hotel')
    city: Mapped['City'] = relationship('City', back_populates='city_hotel')
    service: Mapped['Service'] = relationship('Service', back_populates='service_hotel')
    owner: Mapped['UserProfile'] = relationship('UserProfile', back_populates='hotel_owner')

    images_hotel: Mapped[List['ImageHotel']] = relationship('ImageHotel', back_populates='hotel', cascade='all, delete-orphan')
    room_hotel: Mapped[List['Room']] = relationship('Room', back_populates='hotel', cascade='all, delete-orphan')
    review_hotel: Mapped[List['Review']] = relationship('Review', back_populates='hotel', cascade='all, delete-orphan')
    booking_hotel: Mapped[List['BookingHotel']] = relationship('BookingHotel', back_populates='hotel', cascade='all, delete-orphan')



class ImageHotel(Base):
    __tablename__ = 'image_hotel'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    image: Mapped[str] = mapped_column(String)

    hotel: Mapped['Hotel'] = relationship('Hotel', back_populates='images_hotel')

class Room(Base):
    __tablename__ = 'room'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    room_name: Mapped[str] = mapped_column(String(32))
    room_image: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(SmallInteger, default=0)

    hotel: Mapped['Hotel'] = relationship('Hotel', back_populates='room_hotel')

    images_room: Mapped[List['ImageRoom']] = relationship('ImageRoom', back_populates='room', cascade='all, delete-orphan')
    room_booking: Mapped[List['BookingHotel']] = relationship('BookingHotel', back_populates='room', cascade='all, delete-orphan')

class ImageRoom(Base):
    __tablename__ = 'image_room'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    image: Mapped[str] = mapped_column(String)

    room: Mapped['Room'] = relationship('Room', back_populates='images_room')

class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    stars: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)

    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='user_review')
    hotel: Mapped['Hotel'] = relationship('Hotel', back_populates='review_hotel')

class BookingHotel(Base):
    __tablename__ = 'booking_hotel'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    check_in_date: Mapped[date] = mapped_column(Date)
    check_out_date: Mapped[date] = mapped_column(Date)
    grown_ups: Mapped[int] = mapped_column(SmallInteger, default=0)
    children: Mapped[int] = mapped_column(SmallInteger, default=0)

    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='user_booking')
    hotel: Mapped['Hotel'] = relationship('Hotel', back_populates='booking_hotel')
    room: Mapped['Room'] = relationship('Room', back_populates='room_booking')