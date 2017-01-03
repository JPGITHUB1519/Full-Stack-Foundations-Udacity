from flask import Flask, request, redirect, url_for, render_template, flash, jsonify, session, g
# template_folder -> change folder templates, static_folder = change static folder
app = Flask(__name__, template_folder="templates_finalproject", static_folder="static_finalproject")
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import restaurant_queries 
import fpcrud
from fputility import *
from werkzeug import generate_password_hash, check_password_hash
# choosing database to work
# engine = create_engine('sqlite:///restaurantmenu.db')
# # connection betweens classes and tables
# Base.metadata.bind = engine

# DBSession = sessionmaker(bind = engine)
# session = DBSession()

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

### USER ASKING ###
def getSession():
	""" Check if the user is actually logged"""
	if 'user' in session :
		return session['user']
	return None

@app.before_request
def beforeRequest():
	""" Asking the cookie to the g variable each Request"""
	g.user = None
	if 'user' in session :
		g.user = session['user']

#### API ENDPOINTS ###
@app.route('/restaurants/JSON/')
def showRestaurantsJson():
	""" return Json of all Restaurants """
	restaurants = fpcrud.get_restaurants()
	return jsonify(Restaurants=[restaurant.serialize for restaurant in restaurants])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON/')
def showMenuJson(restaurant_id):
	items = fpcrud.getMenuItemByRestaurant(restaurant_id)
	return jsonify(Items=[item.serialize for item in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def showMenuItem(restaurant_id, menu_id):
	item = fpcrud.getMenuItemById(menu_id)
	return jsonify(item=item.serialize)

### Normal Views ###
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	""" View to Show all Restaurants"""
	if g.user :
		restaurants = fpcrud.get_restaurants()
		return render_template("restaurant.html", 
								restaurants=restaurants)
	else :
		return redirect(url_for('login'))

@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
	""" View to Create a new Restaurant""" 
	if request.method == 'GET':
		return render_template('newrestaurant.html')
	if request.method == 'POST':
		fpcrud.insert_restaurant(request.form['name'], request.form['image_url'])
		return redirect(url_for('showRestaurants'))

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET','POST'])
def editRestaurant(restaurant_id):
	""" View to edit a existing Restaurant"""
	if request.method == 'GET':
		restaurant = fpcrud.get_restaurant_byid(restaurant_id)
		return render_template('editrestaurant.html', 
								restaurant=restaurant,
								restaurant_id=restaurant_id)
	if request.method == 'POST':
		fpcrud.edit_restaurant(restaurant_id, request.form['name'])
		return redirect(url_for('showRestaurants'))

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET','POST'])
def deleteRestaurant(restaurant_id, methods=['GET', 'POST']):
	""" View to delete a Restaurant"""
	if request.method == 'GET':
		restaurant = fpcrud.get_restaurant_byid(restaurant_id)
		return render_template('deleterestaurant.html',
			 					restaurant=restaurant,
			 					restaurant_id=restaurant_id)
	if request.method == 'POST':
		fpcrud.delete_restaurant(restaurant_id)
		return redirect(url_for('showRestaurants'))

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	""" Show Menu of a Restaurant"""
	restaurant = fpcrud.get_restaurant_byid(restaurant_id)
	items = fpcrud.getMenuItemByRestaurant(restaurant_id)
	return render_template('menu.html',
							restaurant_id=restaurant_id,
							restaurant=restaurant, 
							items=items)

@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	""" Making new item for the menu of a rentaurant"""
	if request.method == 'GET':
		return render_template('newmenuitem.html', restaurant_id=restaurant_id)
	if request.method == 'POST':
		fpcrud.insertMenuItem(restaurant_id,
							  request.form["name"],
							  request.form["course"],
							  request.form["description"],
							  request.form["price"],
							  request.form["image_url"]
							  )
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
	""" Editing a item of the menu of a restaurant"""
	restaurant = fpcrud.get_restaurant_byid(restaurant_id)
	item = fpcrud.getMenuItemById(menu_id)
	if request.method == "GET":
		return render_template('editmenuitem.html', 
								item=item,
								restaurant_id=restaurant_id,
								menu_id=menu_id)
	if request.method == "POST":
		fpcrud.editMenuItem(menu_id,
							  request.form["name"],
							  request.form["course"],
							  request.form["description"],
							  request.form["price"],
							  )
		return redirect(url_for('showMenu', restaurant_id=restaurant_id, item=item))

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	""" Deleting a item of the menu of a restaurant"""
	restaurant = fpcrud.get_restaurant_byid(restaurant_id)
	item = fpcrud.getMenuItemById(menu_id)
	if request.method == 'GET':
		return render_template('deletemenuitem.html', 
								item=item,
								restaurant_id=restaurant_id,
								menu_id=menu_id)
	if request.method == 'POST':
		fpcrud.deleteMenuItem(menu_id)
	return redirect(url_for('showMenu', restaurant_id=restaurant_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == "GET" :
		return render_template('login.html')
	if request.method == "POST" :
		# drop session in each request
		session.pop('user', None)
		if fpcrud.authenticateUser(request.form["username"], request.form["password"]):
			session["user"] = request.form["username"]
			return redirect(url_for('showRestaurants'))
		else:
			return render_template('login.html', error_login='Invalid Login')

@app.route('/signup', methods=['GET','POST'])
def signup():
	if request.method == "GET":
		return render_template('signup.html')

	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		verify = request.form["verify"]
		email = request.form["email"]
		error_user = ""
		error_password = ""
		error_verify = ""
		error_email = ""
		error_exits = ""
		cond_error = False

		if not validateUsername(username):
			error_user = "That's not a valid Username"
			cond_error = True
		
		if fpcrud.checkExitsUser(username):
			error_exits = "That's user already Exits"
			cond_error = True

		if not validatePassword(password):
			error_password = "That's not a valid Password"
			cond_error = True
		else :
			if password != verify :
				error_verify = "Password Must be Equal"
				cond_error = True
		if not validateEmail(email):
			error_email = "Invalid Email"
			cond_error = True
		if not cond_error :
			password = generate_password_hash(password)
			fpcrud.insertUser(username, password, email)
			session["user"] = username
			return redirect(url_for('showRestaurants'))

		return render_template('signup.html',
								error_user=error_user,
								error_password=error_password,
								error_verify=error_verify,
								error_email=error_email,
								error_exits=error_exits,
								username=username,
								email=email,
								)

@app.route('/logout')
def logout():
	""" Logout View DELETE THE SESSION VARIABLE FROM THE APP"""
	if not getSession() :
		return redirect(url_for('login'))
	session.pop('user', None)
	return redirect(url_for('login'))

if __name__ == "__main__":
    app.debug = True
    app.secret_key = "PYTHON"
    app.run()