# flask imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# creates Flask object
app = Flask(__name__)
# configuration
# NEVER HARDCODE YOUR CONFIGURATION IN YOUR CODE
# INSTEAD CREATE A .env FILE AND STORE IN I
app.config['SECRET_KEY'] = '2354td46buxtueut'
database_name = 'sql'
default_database_path = "postgresql://{}:{}@{}/{}".format('postgres', 123, 'localhost:5432', database_name)
# database name
app.config['SQLALCHEMY_DATABASE_URI'] = default_database_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# creates SQLALCHEMY object
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Database ORMs
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.String(50), unique=True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(70), unique=True)
	password = db.Column(db.String(80))