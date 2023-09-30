# imports for PyJWT authentication
import jwt
from functools import wraps
from flask import request, jsonify
from models import *


# decorator for verifying the JWT
def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None
		# jwt is passed in the request header
		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']
		# return 401 if token is not passed
		if not token:
			return jsonify({'message': 'Token is missing !!'}), 401

		try:
			# decoding the payload to fetch the stored details
			data = jwt.decode(token, app.config['SECRET_KEY'])
			"""
			{
			"name": "Feven"
			"email":"test@gmail.com",
			"password":"1225636546",
			"public_id": "fev873kd"
            }
			"""
			current_user = User.query\
				.filter_by(public_id=data['public_id'])\
				.first()
	    
		except:
		    return jsonify({
				'message': 'Token is invalid !!'
			}), 401
		# returns the current logged in users context to the routes
		return f(current_user, *args, **kwargs)

	return decorated