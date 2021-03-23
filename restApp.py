#!/usr/bin/env python3
#adapted from Rick's code
from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import Resource, Api, reqparse
from flask_session import Session
from helpers import check_if_admin
import json
from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import *
import pymysql.cursors
import settings # Our server and db settings, stored in settings.py
import ssl #include ssl libraries
import sys

app = Flask(__name__, static_url_path='/static')
app.secret_key = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'peanutButter'
app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST
Session(app)

####################################################################################
#
# Error handlers
#
@app.errorhandler(400) # decorators to add to 400 response
def not_found(error):
	return make_response(jsonify( { "status": "Bad request" } ), 400)

@app.errorhandler(404) # decorators to add to 404 response
def not_found(error):
	return make_response(jsonify( { "status": "Resource not found" } ), 404)

####################################################################################
#
# Static Endpoints for humans
# curl -k https://cs3103.cs.unb.ca:5045/
class Root(Resource):
	def get(self):
		return app.send_static_file('index.html')

####################################################################################
#
# Identify/create endpoints and endpoint objects
#
from authorize import Authorize
from signin import SignIn
from user import User
from users import Users
from folders import Folders
api = Api(app)
api.add_resource(Root,'/')
api.add_resource(SignIn, '/signin')
api.add_resource(Users, '/users')
api.add_resource(User, '/users/<string:email>')
api.add_resource(Folders, '/users/<string:email>/folders')
api.add_resource(Authorize, '/users/<string:email>/authorize')

#############################################################################
if __name__ == "__main__":
	context = ('cert.pem', 'key.pem') # Identify the certificates you've generated.
	app.run(host=settings.APP_HOST, 
		port=settings.APP_PORT, 
		ssl_context=context,
		debug=settings.APP_DEBUG)
