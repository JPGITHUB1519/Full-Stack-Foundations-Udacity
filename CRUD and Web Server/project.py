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
@app.route("/")
# @app.route("/items")
# def restaurants():
#     restaurants = session.query(MenuItem).all()
#     return render_template("menu.html", restaurants)

# Api Stuffs
# Json EndPoint Get all items from a restaurantMenu
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJson(restaurant_id, menu_id):
    item = restaurant_queries.getMenuItemById(menu_id)
    return jsonify(Menuitem=item.serialize)

@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id) 
    return render_template("menu.html", restaurant=restaurant, items=items)

# Task 1: Create route for newMenuItem function here

@app.route("/restaurants/<int:restaurant_id>/new/", methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == "POST" :
        restaurant_queries.insertMenuItem(restaurant_id, 
                       request.form['name'], 
                       request.form['course'], 
                       request.form['description'], 
                       request.form['price'])
        flash("New Menu Item Created")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else :
        return render_template("newmenuitem.html", 
            restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here
@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/edit/", methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'GET':
        item = restaurant_queries.getMenuItemById(menu_id)
        return render_template('editmenuitem.html', 
                                restaurant_id=restaurant_id,
                                item=item)
    if request.method == "POST":
        restaurant_queries.editMenuItem(menu_id, 
                    request.form['name'], 
                    request.form['course'],
                    request.form['description'],
                    request.form['price'])
        flash("Menu Item has been Edited")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))


# Task 3: Create a route for deleteMenuItem function here
@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/delete/", methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'GET' :
        item = restaurant_queries.getMenuItemById(menu_id)
        return render_template("deletemenuitem.html",
                                restaurant_id=restaurant_id,
                                item=item)
    if request.method == 'POST':
        restaurant_queries.deleteMenuItem(menu_id)
        flash("Menu Item has been Deleted")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

@app.route("/test")
def test():
    # @app.route("/restaurants/<int:restaurant_id>/new/", methods=['GET', 'POST'])
    # url for(<function_name>, paraemeter1 = value, parameter_n = value_n)
    # url for is useful when when want to change our url and not change in all parts
    return redirect(url_for('newMenuItem', restaurant_id=1))

if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run()