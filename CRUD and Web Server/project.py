from flask import Flask, request, redirect, url_for, render_template
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

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id) 
    return render_template("menu.html", restaurant=restaurant, items=items)

# Task 1: Create route for newMenuItem function here

@app.route("/restaurants/<int:restaurant_id>/new/", methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == "GET" : 
        output = ""
        # print html
        output += "<html><head><title>Create Menu Item</title></head><body>" \
        "<h1>Create new Menu Item</h1>" \
        "<form method='post' action='/restaurants/%s/new/'>" \
        "<div><label>Name<input type='text' name='name'></label></div>" \
        "<div><label>Course </label><input type='text' name='course'></label></div>" \
        "<div><label>Description </label><input type='text' name='description'></div>" \
        "<div><label>Price <input type='text' name='price'</label></div>" \
        "<div><input type='submit' name='Submit'></div>" \
        "</form>" \
        "</body><html>" % restaurant_id
        return output

    if request.method == "POST" :
        restaurant_queries.insertMenuItem(restaurant_id, 
                       request.form['name'], 
                       request.form['course'], 
                       request.form['description'], 
                       request.form['price'])
        return redirect('/items')

# Task 2: Create route for editMenuItem function here
@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/edit/", methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'GET':
        item = restaurant_queries.getMenuItemById(menu_id)
        output = ""
        # print html
        output += "<html><head><title>Create Menu Item</title></head><body>" \
        "<h1>Create new Menu Item</h1>" \
        "<form method='post' action='/restaurants/%s/%s/edit/'>" \
        "<div><label>Name<input type='text' name='name' value=%s></label></div>" \
        "<div><label>Course </label><input type='text' name='course' value='%s'></label></div>" \
        "<div><label>Description </label><input type='text' name='description' value='%s'></div>" \
        "<div><label>Price <input type='text' name='price' value='%s'</label></div>" \
        "<div><input type='submit' name='Submit'></div>" \
        "</form>" \
        "</body><html>" % (restaurant_id, menu_id, item.name, item.course, item.description, item.price)
        return output

    if request.method == "POST":
        editarMenuItem(menu_id, 
                    request.form['name'], 
                    request.form['course'],
                    request.form['description'],
                    request.form['price'])
        return redirect('/items')


# Task 3: Create a route for deleteMenuItem function here
@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/delete/", methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'GET' :
        item = restaurant_queries.getMenuItemById(menu_id)
        output = ""
        output += "<html><head></head><body>" \
        "<h1>Delete Menu Item</h1>" \
        "<p><b>Name : </b>%s</p>" \
        "<p><b>Course: </b>%s</p>" \
        "<p><b>Description : </b>%s</p>" \
        "<p><b>Price: </b>%s</p>" \
        "<h2>Are you Sure you want do delete this from the Menu Items?" \
        "<form method='post' action='/restaurants/%s/%s/delete/'>" \
        "<input type='submit' value='Delete'></form>" \
        % (item.name, item.course, item.description, item.price, restaurant_id, menu_id)
        return output
    if request.method == 'POST':
        restaurant_queries.deleteMenuItem(menu_id)
        return redirect('/items')

if __name__ == "__main__":
    app.debug = True
    app.run()