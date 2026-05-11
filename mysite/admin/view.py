from db.models import UserProfile, Country, City
from sqladmin import ModelView

class UserProfileView(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.username, UserProfile.email]

class CountryView(ModelView, model=Country):
    column_list = [Country.id, Country.country_name]

class CityView(ModelView, model=City):
    column_list = [City.id, City.city_name]