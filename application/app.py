from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
from routes import routes
from flask_migrate import Migrate

migrate = Migrate()

def init_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config['SECRET_KEY'] = 'CHANGE_FOR_PRODUCTION'
    
    #config app (DATABASE)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True # Shows corresponding SQL queries


    # initialize app with the current database
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
    

    # register routes (add enpoints / pages to the application)
    app.register_blueprint(routes)

    with app.app_context():
        db.create_all()  # Create sql tables for our data models

        return app

app = init_app()
