from flask import Flask, render_template

app = Flask(__name__)

# URL PATHS
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/create", methods=['GET','POST'])
def creating_order():
    if request.method == 'POST':
        return "<h1>POST method triggered</h1>"
    return "<p>create order</p>"

@app.route("/processing")
def order_processing():
    return "<h1>order processing</h1>"

@app.route("/complete")
def complete_orders():
    return "<h1>complete orders</h1>"