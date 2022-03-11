from flask import request, render_template, redirect, Blueprint, flash
from models import User, Order
from app import db
from twilio.rest import Client
import speech_recognition as sr
import time 

account_sid = 'ACb9b69fcad32c0d9fd02fea6c8fad4a70'
auth_token = 'f56940ec6b359efaab4a7b5f77eb3adf'
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
                
                GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{
                    "type": "service_account",
                    "project_id": "scap-hackathon",
                    "private_key_id": "fee187bf48da677a28a178b8f7547aa7b13c3be1",
                    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCZFWUynwXwtNXm\ncyZoP623psUJLJ9gxgUUo05J1fHLA9g2nfz8hkMK1EpwylHb6SsRuuGNNbEwrt/S\nBnZ0YdGu/UlrQ0XhEHzeJbB5LYni6geoPX0iePaw3dj8ddxUQujRDUqxFMv31lma\n7B/vKkqPGDN1F1Tl5xThXriAt6ceHXFUGqy3FGusXZ1+f3xFlMT7ObKP05kGzIsH\nxAhOeGTPmbD/Evw7jOXePWG60mI7E5lmtZMRYJ7jRn9kF8cmbsLZ1dOWCUskI//Z\nvOy/mcBVOmfAGcwqn9NSHLWKw3TRYEk0XMmrMeBMqlxpGejSPGLaEG2AkIrI2iLk\nfRyY1L7tAgMBAAECggEACJB4XWklKW7MiryFeQ6a9uvXGSjMb9sUPK/YOOxFv0Bj\nT8bt+OjABnKTCZVgGAgG91J3vPE0jQ8ziWoAJYm1c+9KtLwKREmqWrlMErN4A+Bo\n9kIeZpfS4VlAAvvLDFHD+bIfLCIIOUDeOXsdXEGG81N8yX+5KbWQZv1oIBdmO5p+\n2EfvkJ7zyFM164zeNdKuY+G7k3rEotX7CRFpvNV7wuf2h9DYNFSlBk4NYiNbFxZb\nYLHq+uOsCrgyKwPq47Evn9ogqZcvUNB5d9/8CqF8R+xUanzOc4ijqje1OzPNQt5F\nRrpXf09/28QgFIuTxFObFC/BH+dxqA3Rs0mdhCX2kQKBgQDYTwEwHbbV9tBkBwUo\nr2A+sbpb7jsS0glFomkn5TKzJeVysqo3ztjpRnaQx9umP8kZPcckJywmhQlBREGa\noer04qhcKcml6IL1Mbf+fub/2OBWm/f8ulYw/dstK4O+ORveTBjctmtpE/CjGb8j\nF3EO5GYCr3a+szRUa//0O1lWZQKBgQC1LGyeqv6Hnu4VoVDMrbUn0H0JiJxSSWMI\nBQFPM1HfBQPGOJ+lPLYgWE27mvjiANhzK2Ovniis2LB0rMzKIbZeNrt7bB6gYWHV\nZKUbUHnaiRYkWtJSrdQuQtgtBF/DiOeCnJsMBBns4w5JyxoYlFTh9LMoebbtClac\ngYsrqcxZ6QKBgBahxYUMRtoCNfGRTnfgSZilrdL6jRG+ChxQDuKOt4xI9cXXbbnj\nGYzmw3cIgjHV0KukbBabRqJNHxfGFXshX9z5bhYehSuntTQEXLTzACZawbYuIXc+\n48/Cb9E9EU6w2PqcSammKHzZCj92bSo1xK2DNi0nwKvZQitnFWOvZfyFAoGBAIXj\n8836zqoJoSfpFJ5+zX9EC/PsuqHxTDeUA1i1s46e1SA7nnft+ybCO4gmykGzoELU\n0RHrT2IVrao8Pggvi+fqiPl4eNXLwhKDE6Ww/qyrXOq3F/I0NreNfNcgAWmvFnCn\nLcpeiY5QarHMYFfD30sxnOmPsclSN5nn/qLhFH1pAoGAZ8G1R0F8cBIW5PxIVbYB\nrGYnUyFcXvP1OXugkxOnxqZsy7TYlYOE0yIy29DvW+VyV//jmnVm4M1Loq1I01mv\n6jwODxl1QMwMvRnFVuLsFRQ2nDyB8BZRi2SQzBuCoCUMfxNL9t5XqTyPOaGBGKu+\nU7S/wo3eIkrBrwjcn6UKx2I=\n-----END PRIVATE KEY-----\n",
                    "client_email": "scap-567@scap-hackathon.iam.gserviceaccount.com",
                    "client_id": "112546786135886116997",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/scap-567%40scap-hackathon.iam.gserviceaccount.com"
                                    }"""
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
