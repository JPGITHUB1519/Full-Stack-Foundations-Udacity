from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
# choosing database to work
engine = create_engine('sqlite:///restaurantmenu.db')
# connection betweens classes and tables
Base.metadata.bind = engine
# creating session to connect databae
DBSession = sessionmaker(bind = engine)
session = DBSession()
myFirstRestaurant = Restaurant(name="Pizza Doug")
# is stagging to add to the database
session.add(myFirstRestaurant)
# save in database
session.commit()
# select Restaurant
print session.query(Restaurant).all()
chessPizza = MenuItem(name="Chesse Pizza",
					  description="Made with all naturals ingredients and fresh mozarella",
					  course="Entree",
					  price="$8.99",
					  restaurant=myFirstRestaurant)
session.add(chessPizza)
session.commit()
print session.query(MenuItem).all() 