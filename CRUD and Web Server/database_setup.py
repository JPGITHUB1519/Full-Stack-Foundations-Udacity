import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from werkzeug import generate_password_hash, check_password_hash

Base = declarative_base()

class Restaurant(Base):
	__tablename__ = 'restaurant'
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)

	@property 
	def serialize(self):
		return {
			'id' : self.id,
			'name' : self.name
		} 

class MenuItem(Base):
	__tablename__ = 'menu_item'
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	course = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)

	# We added this serialize function to be able to send JSON objects in a
	# serializable format
	@property
	def serialize(self):
		# return dictionary
		return {
			'name' : self.name,
			'description' : self.description,
			'id' : self.id,
			'price' : self.price,
			'course' : self.course
			}

class User(Base):
	__tablename__ = 'user'
	idusuario = Column(Integer, primary_key = True)
	username = Column(String(50), unique=True)
	password = Column(String(50))
	email = Column(String(50))
	is_active = Column(Boolean, default=True)
	is_admin = Column(Boolean, default=False)

	def setPassword(self, password):
		""" Set an hashed password from werzeugh method"""
		self.password = generate_password_hash(password)

	def checkPassword(self, password):
		""" Check if a password matches a hash"""
		return check_password_hash(self.password, password)

### insert at end of the line ###
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)