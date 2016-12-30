from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
# choosing database to work
engine = create_engine('sqlite:///restaurantmenu.db')
# connection betweens classes and tables
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

spinach = session.query(MenuItem).filter_by(name='Spinach Ice Cream').one()
# deleting
session.delete(spinach)
session.commit()
spinach = session.query(MenuItem).filter_by(name='Spinach Ice Cream').one()
print spinach

# delete steps
"""
	1. get record
	2. session.delete(record)
	3. session.commit()

	on resume
	Find the entry
	Session.delete(Entry)
	Session.commit()
"""
