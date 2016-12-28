from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
# choosing database to work
engine = create_engine('sqlite:///restaurantmenu.db')
# connection betweens classes and tables
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for veggieBurger in veggieBurgers :
	veggieBurger.price = "$55.50"
	session.add(veggieBurger)
	session.commit()

# update steps
"""
	1. get record
	2. set new value to the columns of the records
	3. add value to session
	4. session.commit()
	
	on resume :
		Find Entry
		Reset value(s)
		Add to session
		Execute session.commit()
"""
