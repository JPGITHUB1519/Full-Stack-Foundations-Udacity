from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
# choosing database to work
engine = create_engine('sqlite:///restaurantmenu.db')
# connection betweens classes and tables
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()
restaurant = session.query(Restaurant).first()
print restaurant.name, restaurant.id
# get all restaurant names
items = session.query(MenuItem).all()
for item in items :
	print "Name : " + item.name + " Price : " + item.price

