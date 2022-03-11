from flask import request, render_template, redirect, Blueprint, flash
from models import User, Order
from app import db
from twilio.rest import Client
import speech_recognition as sr
import time 


client = Client(account_sid, auth_token)

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
    return render_template('index.html')

def creating_order():
    # a POST request sends a data payload to the server (usually on a form submission)
    if request.method == 'POST':
        print('create')
        print(request.form)
        username = request.form['username']
        items = request.form['items']

        if not username:
            flash('Customer Name is Required is required!')
        elif not items:
            flash('Content is required!')
        else:
            #save item and redirect
            try:
                associated_customer = User.query.filter_by(username=username).first()

               
                new_order = Order(user_id=associated_customer.username, items=items)
                
                db.session.add(new_order)
                db.session.commit()
                return render_template('processing.html', orders=Order.query.filter(Order.iscomplete==False).all())
            except:
                flash('invalid customer name (Customer not in the system)')
                return redirect('/')
    else:
        return render_template('processing.html', orders=Order.query.filter(Order.iscomplete==False).all())

def order_processing():
    return render_template('processing.html', orders=Order.query.filter(Order.iscomplete==False).all())

def complete_an_order():
    if request.method== 'POST':
        #get orderid (value) from post request submission
        print("in /create --- Method POST")
        orderid = request.form['Complete_Order']
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
        

        try:
            order = Order.query.filter(Order.id==orderid).first()

            if not order:
                flash('Order does not seem to exist!')

            user = User.query.filter(User.username==order.user_id).first()

            if not user:
                flash('Customer is not found for order!')

            if user.optedin == True:
                #perform API call
                
                # Instantiates a client
                r = sr.Recognizer()
                with sr.AudioFile('./audio.wav') as source:
                    audio = r.record(source)
                
                GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""INSERT JSON OBJECT HERE"""
                try:
                    transcription = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
                except sr.UnknownValueError:
                    print("Google Cloud Speech could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Cloud Speech service; {0}".format(e))

                testmessage = "Customer Name: " + user.username + "\n" + "Order: " + order.items + "\n" + transcription;# order.items user.username
                print(testmessage)
                
                try:
                    message = client.messages.create(
                                    body=str(testmessage),
                                    from_='+14015922644',
                                    to=str(user.phonenumber)
                                )
               
                    print(message.sid)
                except:
                    print("twilio failed")

                

            order.iscomplete = True
            db.session.add(order)
            db.session.commit()
            return redirect("/complete")
        except:
            return 'There was an error for the order CONFIRMATION process'

    else:
        return render_template('completed.html', complete_orders=Order.query.filter(Order.iscomplete==True).all())

def complete_orders():
    return render_template('completed.html', complete_orders=Order.query.filter(Order.iscomplete==True).all())

# register call back function upon visiting particular url
routes = Blueprint("routes", __name__)
routes.route('/')(index)
routes.route("/create", methods=['POST'])(creating_order)
routes.route('/confirm', methods=['POST'])(complete_an_order)
routes.route("/processing")(order_processing)
routes.route("/complete")(complete_orders)
