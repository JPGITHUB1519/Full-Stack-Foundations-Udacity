from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, User
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

def insert_restaurant(name, image_url):
	""" Insert a Restaurant """
	if not image_url :
		# if not exits image, put a placeholde
		image_url = "http://placehold.it/300x300"
	resturant = Restaurant(name=name, image_url=image_url)
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

def insertMenuItem(restaurant_id, name, course,description, price, image_url):
	""" Insert a new Item to the menu of a restaurant """
	if not image_url :
		# if not exits image, put a placeholde
		image_url = "http://placehold.it/300x300"
	item = MenuItem(restaurant_id=restaurant_id, 
					name=name,
					course=course,
					description=description,
					price=price,
					image_url = image_url)
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

########## User CRUD ##########
def insertUser(username, password, email):
	""" Create a new  normal User"""
	user = User(username=username, password=password, email=email)
	session.add(user)
	session.commit()

def insertAdminUser(username, password, email):
	""" Create an admin user"""
	user = User(username=username, password=password, email=email, is_admin=True)
	session.add(user)
	session.commit()

def editUser(old_username, new_username, password, email):
	""" Edit an existing User"""
	user = session.query(User).filter_by(username=old_username).one()
	user.username = new_username
	user.password = password
	user.email = email
	session.add(user)
	session.commit()

def desactivateUser(username):
	""" Desactivate User"""
	user = session.query(User).filter_by(username=username).one()
	user.is_active = False
	session.add(user)
	session.commit()

def activateUser(username):
	""" Activate User"""
	user = session.query(User).filter_by(username=username).one()
	user.is_active = True
	session.add(user)
	session.commit()

def deleteUser(username):
	""" Delete a User"""
	user = session.query(User).filter_by(username=username).first()
	session.delete(user)
	session.commit()

def checkExitsUser(username):
	""" Check if a user Exits"""
	user = session.query(User).filter_by(username=username).first()
	if user :
		return True
	return False

def authenticateUser(username, password):
	""" Authentica a user """
	user =  session.query(User).filter_by(username=username).first()
	if user and user.checkPassword(password):
		return True
	return False



# ########## Testing Zone ##########
# for i in getMenuItemByRestaurant(2) :
# 	print i.name