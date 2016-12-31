from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
# choosing database to work
engine = create_engine('sqlite:///restaurantmenu.db')
# connection betweens classes and tables
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

# restaurant
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

# menu item

def getMenuItems():
	items = session.query(MenuItem).all()
	return items

def getMenuItemById(idmenuitem):
	item = session.query(MenuItem).filter_by(id=idmenuitem).one()
	return item

def insertMenuItem(restaurant_id, name, course,description, price):
	item = MenuItem(restaurant_id=restaurant_id, 
					name=name,
					course=course,
					description=description,
					price=price)
	session.add(item)
	session.commit()


def editMenuItem(idmenu, name, course, description, price):
	item = getMenuItemById(idmenu)
	item.name = name
	item.course = course
	item.description = description
	item.price = price
	session.add(item)
	session.commit()

def deleteMenuItem(idmenu):
	item = getMenuItemById(idmenu)
	session.delete(item)
	session.commit()
#EditMenuItem(1, 'Chorizo', 'salida', 'Queso Delicioso', 500)

#deleteMenuItem(63)


