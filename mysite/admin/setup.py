from fastapi import FastAPI
from sqladmin import Admin
from db.database import engine
from .view import UserProfileView, CountryView, CityView

def setup_admin(app: FastAPI):
    admin = Admin(app, engine=engine)
    admin.add_view(UserProfileView)
    admin.add_view(CountryView)
    admin.add_view(CityView)