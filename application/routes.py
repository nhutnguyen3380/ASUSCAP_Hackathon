from flask import request, render_template, redirect, Blueprint
from models import User, Order, Item

# NOTICE: FLASK follows a MVT (Model-View-Template) like Architectural Design Pattern
# This file defines the Views (and routing):
#   essentially we code out the action (HTTP methods + OUr defined callback) 
#   that we want to occur/display on each URL endpoint (routing)
#   this could be a POST request to create a new order
#   a GET request to retrieve data
#   or a simple navigation to a new page among other things 

# define call back functions
# when a particular URL is visited (see routes below), the following subscribed function will be called
def index():
    return render_template('index.html', users=User.query.all())

def creating_order():
    # a POST request sends a data payload to the server (usually on a form submission)
    if request.method == 'POST':
        return "<h1>POST method triggered</h1>"
    return "<p>create order</p>"

def order_processing():
    return render_template('processing.html')

def complete_orders():
    return render_template('completed.html')

# register call back function upon visiting particular url
routes = Blueprint("routes", __name__)
routes.route('/')(index)
routes.route("/create", methods=['GET','POST'])(creating_order)
routes.route("/processing")(order_processing)
routes.route("/complete")(complete_orders)
