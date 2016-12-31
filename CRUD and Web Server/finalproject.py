from flask import Flask, request, redirect, url_for, render_template, flash, jsonify
app = Flask(__name__)
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

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	""" View to Show all Restaurants"""
	return "This page will show all my Restaurants"

@app.route('/restaurant/new/')
def newRestaurant():
	""" View to Create a new Restaurant""" 
	return "This page will be for making a new restaurant"

@app.route('/restaurant/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
	""" View to edit a existing Restaurant"""
	return "This page will be for editing restaurant %s" % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
	""" View to delete a Restaurant"""
	return "This page will be for deleting restaurant %s" % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	""" Show Menu of a Restaurant"""
	return "This page is the menu for the restaurant %s" % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/menu/new/')
def newMenuItem(restaurant_id):
	""" Making new item for the menu of a rentaurant"""
	return "This page is for making a new menu item for restaurant %s" % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
	""" Editing a item of the menu of a restaurant"""
	return "This page is for editing menu item %s" % menu_id

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
	""" Deleting a item of the menu of a restaurant"""
	return "This page is for deleting menu item %s" % menu_id

if __name__ == "__main__":
    app.debug = True
    app.run()