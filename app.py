from flask import Flask, request, jsonify, make_response
import uuid  # for public id
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_cors import CORS
from .models import app, setup_db, db, db_drop_and_create_all
from .models import User
from .middleware.jwt import token_required,jwt


@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
	# querying the database
	# for all the entries in it
	users = User.query.all()
	# converting the query objects
	# to list of jsons

	output = []
	for user in users:
		# appending the user data json
		# to the response list
		output.append({
			'public_id': user.public_id,
			'name': user.name,
			'email': user.email
		})

	return jsonify({'users': output})

# route for logging user in
@app.route('/login', methods=['POST'])
def login():
	# creates dictionary of form data
	auth = request.form

	if not auth or not auth.get('email') or not auth.get('password'):
		# returns 401 if any email or / and password is missing
		return make_response(
			'Could not verify',
			401,
			{'WWW-Authenticate': 'Basic realm ="Login required !!"'}
		)

	user = User.query\
		.filter_by(email = auth.get('email'))\
		.first()

	if not user:
		# returns 401 if user does not exist
		return make_response(
			'Could not verify',
			401,
			{'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
		)
	#
	if check_password_hash(user.password, auth.get('password')):
		# generates the JWT Token
		token = jwt.encode({
			'public_id': user.public_id,
			'exp' : datetime.utcnow() + timedelta(minutes=30)
		}, 
		app.config['SECRET_KEY']
		)

		return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
	# returns 403 if password is wrong
	return make_response(
		'Could not verify',
		403,
		{'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
	)

# signup route
@app.route('/signup', methods=['POST'])
def signup():
	# creates a dictionary of the form data
	data = request.form

	# gets name, email and password
	name, email = data.get('name'), data.get('email')
	password = data.get('password')

	# checking for existing user
	user = User.query\
		.filter_by(email=email)\
		.first()
	if not user:
		# database ORM object++++++
		user = User(
			public_id=str(uuid.uuid4()),
			name=name,
			email=email,
			password=generate_password_hash(password)
		)
		# insert user
		user.insert()

		return make_response('Successfully registered.', 201)
	else:
		# returns 202 if user already exists
		return make_response('User already exists. Please Log in.', 202)

def create_app(app,test_test_config=None):
    app.config['SECRET_KEY']='57324676734hjvbedhjewr9pp942312y89r321g8t7'
    with app.app_context():
        setup_db(app)
        CORS(app)
        db_drop_and_create_all() 
    return app
    
APP=create_app(app)

if __name__ == "__main__":
    # Retrieve the port number from the environment variable or use 5000 as the default
    port = int(os.environ.get("PORT", 5000))
    # Run the Flask app with the specified host and port
    APP.run(host='127.0.0.1', port=port, debug=True)
