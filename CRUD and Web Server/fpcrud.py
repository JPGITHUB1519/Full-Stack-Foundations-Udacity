from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
# choosing database to work
engine = create_engine('sqlite:///restaurantmenu.db')
# connection betweens classes and tables
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

########## Restaurant CRUD ##########
def get_restaurants() :
	""" Get all the restaurants """
	restaurants = session.query(Restaurant).all()
	return restaurants

def get_restaurant_byid(idrestaurant):
	""" Get one Restaurant by his id """
	restaurant = session.query(Restaurant).filter_by(id=idrestaurant).first()
	return restaurant

def insert_restaurant(name):
	""" Insert a Restaurant """
	resturant = Restaurant(name=name)
	session.add(resturant)
	session.commit()

def edit_restaurant(idrestaurant, name):
	""" Edit a restaurant """
	restaurant = get_restaurant_byid(idrestaurant)
	restaurant.name = name
	session.add(restaurant)
	session.commit()

def delete_restaurant(idrestaurant):
	""" Delete a Restaurant """
	restaurant = get_restaurant_byid(idrestaurant)
	session.delete(restaurant)
	session.commit()

########## Menu Items CRUD ##########

def getMenuItems():
	""" Get all Menu Items """
	items = session.query(MenuItem).all()
	return items

def getMenuItemById(idmenuitem):
	""" Get a menu Item By Id """
	item = session.query(MenuItem).filter_by(id=idmenuitem).one()
	return item

def getMenuItemByRestaurant(idrestaurant):
	""" Get the menu of a Restaurant """
	items = session.query(MenuItem).filter_by(restaurant_id=idrestaurant).all()
	return items

def insertMenuItem(restaurant_id, name, course,description, price):
	""" Insert a new Item to the menu of a restaurant """
	item = MenuItem(restaurant_id=restaurant_id, 
					name=name,
					course=course,
					description=description,
					price=price)
	session.add(item)
	session.commit()


def editMenuItem(idmenu, name, course, description, price):
	""" Edit a menu item """
	item = getMenuItemById(idmenu)
	item.name = name
	item.course = course
	item.description = description
	item.price = price
	session.add(item)
	session.commit()

def deleteMenuItem(idmenu):
	""" Delete a item item from the menu"""
	item = getMenuItemById(idmenu)
	session.delete(item)
	session.commit()


# ########## Testing Zone ##########
# for i in getMenuItemByRestaurant(2) :
# 	print i.name