from flask import request, render_template, redirect, Blueprint, flash
from models import User, Order, Item
from app import db

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
        username = request.form['username']
        #content = request.form['content']

        if not username:
            flash('Customer Name is Required is required!')
        #elif not content:
            #flash('Content is required!')
        else:
            #save item and redirect
            try:
                associated_customer = User.query.filter_by(username=username).first()

                new_order = Order(user_id=associated_customer.id)
                an_item = Item(text="sample item", order_id=new_order.id)
                db.session.add(new_order)
                db.session.add(an_item)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an error for the order creation process'
    else:
        return render_template('processing.html', orders=Order.query.filter(Order.iscomplete==False).all())

    


def order_processing():
    return render_template('processing.html', orders=Order.query.filter(Order.iscomplete==False).all())

def complete_an_order():
    if request.method== 'POST':
        #get orderid (value) from post request submission
        orderid = request.form['Complete_Order']

        try:
            order = Order.query.filter(Order.id==orderid).first()
        

            if not order:
                flash('Order does not seem to exist!')

            user = User.query.filter(User.id==order.user_id).first()
            print(user.id)

            if not user:
                flash('Customer is not found for order!')

            if user.optedin == True:
                #perform API call
                print('API called here')

            order.iscomplete = True
            db.session.add(order)
            db.session.commit()
            return render_template('completed.html', complete_orders=Order.query.filter(Order.iscomplete==True).all())
        except:
            return 'There was an error for the order CONFIRMATION process'

    else:
        return render_template('processing.html', orders=Order.query.filter(Order.iscomplete==False).all())

def complete_orders():
    return render_template('completed.html', complete_orders=Order.query.filter(Order.iscomplete==True).all())

# register call back function upon visiting particular url
routes = Blueprint("routes", __name__)
routes.route('/')(index)
routes.route("/create", methods=['POST'])(creating_order)
routes.route('/confirm', methods=['POST'])(complete_an_order)
routes.route("/processing")(order_processing)
routes.route("/complete")(complete_orders)
