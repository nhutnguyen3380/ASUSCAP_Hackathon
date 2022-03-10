from flask_sqlalchemy import  SQLAlchemy
from sqlalchemy import false
# reference https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#quickstart

# This defines models to be used by an ORM (Object Relational Mapper)
# ORMs are used to automatically create all the basic queries and mutations of an object in SQL
# in the form of extremely easy to use function calls
db = SQLAlchemy()

# define the entities for the project

class User(db.Model):
    ''' 
    USER entity
    fields: username (pk), phonenumber, orders, optedin
    '''
    username = db.Column(db.String(80), primary_key=True)
    phonenumber = db.Column(db.String(12), unique=True, nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)
    optedin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User: %r, # %r, optedin: %r>' % (self.username, self.phonenumber, self.optedin)

class Order(db.Model):
    ''' 
    Order entity
    fields: id, user_id, items, iscomplete
    '''
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), db.ForeignKey('user.username'))
    items = db.Column(db.String(120), nullable=False)
    iscomplete = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Order: id# %r complete?: %r>' % (self.id, self.iscomplete)

# class Item(db.Model):
#     '''
#     Item Entity
#     fields: id, order_id, text
#     '''
#     id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
#     text = db.Column(db.String(80), nullable=False)

#     def __repr__(self):
#         return '<Item: %r>' % (self.text)