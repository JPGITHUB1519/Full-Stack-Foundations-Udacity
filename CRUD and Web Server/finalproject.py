from flask import Flask, request, redirect, url_for, render_template, flash, jsonify
# template_folder -> change folder templates, static_folder = change static folder
app = Flask(__name__, template_folder="templates_finalproject", static_folder="static_finalproject")
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import restaurant_queries 
# choosing database to work
engine = create_engine('sqlite:///restaurantmenu.db')
# connection betweens classes and tables
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

#Fake Restaurants
restaurant = {'name':'KFC', 'id':'2', 'image' : 'https://upload.wikimedia.org/wikipedia/en/thumb/b/bf/KFC_logo.svg/1024px-KFC_logo.svg.png'}

restaurants = [
				{'name': 'Burger King', 'id': '1', 'image' : 'https://pbs.twimg.com/profile_images/694921357864386563/p0nF8Bj8.jpg'}, 
				{'name':'KFC', 'id':'2', 'image' : 'https://upload.wikimedia.org/wikipedia/en/thumb/b/bf/KFC_logo.svg/1024px-KFC_logo.svg.png'},
				{'name':'Taco Hut', 'id':'3', 'image' : 'http://img01.deviantart.net/8e84/i/2003/38/6/9/taco_hut.jpg'}]


#Fake Menu Items
items = [ 
	{'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1', 'image':"http://uploads.ecbilla.com/1466/product/3061-cheese-pizza-product-1.png"}, 
	{'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2', 'image':"http://www.bbcgoodfood.com/sites/default/files/chocolate-avocado-cake.jpg"},
	{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3', 'image':"http://www.seriouseats.com/images/2013/10/20131009-caesar-salad-food-lab-12.jpg"},
	{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4', 'image':'https://drinkedin.net/images/easyblog_images/62/Long-Island-Ice-Tea.jpg'},
	{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5', 'image' : 'https://www.aldi.us/fileadmin/fm-dam/Recipes/Appetizers/SpinachDip_D.jpg'} ]

item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree', 'image':"http://uploads.ecbilla.com/1466/product/3061-cheese-pizza-product-1.png"}

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	""" View to Show all Restaurants"""
	return render_template("restaurant.html", restaurants=restaurants)

@app.route('/restaurant/new/')
def newRestaurant():
	""" View to Create a new Restaurant""" 
	return render_template('newrestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
	""" View to edit a existing Restaurant"""
	return render_template('editrestaurant.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
	""" View to delete a Restaurant"""
	return render_template('deleterestaurant.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	""" Show Menu of a Restaurant"""
	return render_template('menu.html', restaurant=restaurant, items=items)

@app.route('/restaurant/<int:restaurant_id>/menu/new/')
def newMenuItem(restaurant_id):
	""" Making new item for the menu of a rentaurant"""
	return render_template('newmenuitem.html')

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
	""" Editing a item of the menu of a restaurant"""
	return render_template('editmenuitem.html', item=item)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
	""" Deleting a item of the menu of a restaurant"""
	return render_template('deletemenuitem.html', item=item)

if __name__ == "__main__":
    app.debug = True
    app.run()