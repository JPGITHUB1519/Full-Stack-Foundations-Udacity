from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
# choosing database to work
engine = create_engine('sqlite:///restaurantmenu.db')
# connection betweens classes and tables
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

# raw sql all
data = session.execute("Select * from restaurant")
for i in data :
	print i.name

# raw sql one
# one
data = session.execute("Select * from restaurant where id = :var", {'var':1})
print data.fetchone().name