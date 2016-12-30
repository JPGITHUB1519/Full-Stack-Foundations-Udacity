from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
# choosing database to work
engine = create_engine('sqlite:///restaurantmenu.db')
# connection betweens classes and tables
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

def get_restaurants() :
	restaurants = session.query(Restaurant).all()
	return restaurants

def get_restaurant_byid(idrestaurant):
	restaurant = session.query(Restaurant).filter_by(id=idrestaurant).first()
	return restaurant

def insert_restaurant(name):
	resturant = Restaurant(name=name)
	session.add(resturant)
	session.commit()

def edit_restaurant(idrestaurant, name):
	restaurant = get_restaurant_byid(idrestaurant)
	restaurant.name = name
	session.add(restaurant)
	session.commit()
def delete_restaurant(idrestaurant):
	restaurant = get_restaurant_byid(idrestaurant)
	session.delete(restaurant)
	session.commit()

edit_restaurant(17, 'value')



