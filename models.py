# flask imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# creates Flask object
app = Flask(__name__)
# creates SQLALCHEMY object
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Setup the database for the Flask app.
def setup_db(app):
    # Database configuration.
    database_name = 'sql'
    default_database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'nata@2003', 'localhost:5432', database_name)
    app.config['SQLALCHEMY_DATABASE_URI'] = default_database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Set up the database with the app.
    db.app = app
    db.init_app(app)

# Drop and create all tables in the database.
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

# Database ORMs
class User(db.Model):

    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(80))
    
    def __init__(self, public_id, name,email,password):
        self.public_id = public_id
        self.name = name
        self.email = email
        self.password = password

    def insert(self):
        # Add the user instance to the database session and commit changes.
        db.session.add(self)
        db.session.commit()

    def update(self):
        # Commit changes to update the user in the database.
        db.session.commit()

    def delete(self):
        # Delete the user from the database.
        db.session.delete(self)
        db.session.commit()

    
    def format_record(self):
        # Format the user data to a dictionary.
        return {
            'id': self.id,
            'public_id': self.public_id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
        }
