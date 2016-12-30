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

restaurants = get_restaurants()
for restaurant in restaurants :
	print restaurant.name
