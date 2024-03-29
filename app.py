#!/usr/bin/env python3
#adapted from Rick's code
#the application directory structure for the server is given by the organization of this submission folder
#this folder (repo) can go on your home drive on the cs3103 machines
from flask import Flask, jsonify, abort, request, make_response, session, send_file
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
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='/audio/static')
app.secret_key = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
if(settings.APP_HOST != '127.0.0.1'):
	app.config['SESSION_COOKIE_NAME'] = 'peanutButter'
	app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST
app.config['UPLOAD_FOLDER'] = settings.UPLOAD_FOLDER
# app.config['SESSION_COOKIE_DOMAIN'] = 'localhost:5045'
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
		print('hello')
		# session["test"] = "hi"
		# return 'init'
		return app.send_static_file('index.html')

class Info(Resource):
	def get(self):
		return send_file(filename_or_fp=settings.STATIC_FOLDER+'/openapi/index.html')
		# return app.send_static_file('openapi/index.html')

# class Test(Resource):
# 	def get(self):
# 		return 'hi=' + session.get('test', 'no test')
# 		# return send_file('1', attachment_filename='1')
####################################################################################
#
# Identify/create endpoints and endpoint objects
#
from authorize import Authorize
from signin import SignIn
from user import User
from users import Users
from folders import Folders
from folder import Folder
from files import Files
from file import File
api = Api(app)
root = '/audio' #'/Audīsne mē?'
api.add_resource(Root,root)
api.add_resource(Info,root+'/info')
# api.add_resource(Test,root+'/test')
api.add_resource(SignIn, root+'/signin')
api.add_resource(Users, root+'/users')
api.add_resource(User, root+'/users/<string:email>')
api.add_resource(Authorize, root+'/users/<string:email>/authorize')
api.add_resource(Folders, root+'/users/<string:email>/folders')
api.add_resource(Folder, root+'/users/<string:email>/folders/<int:folder>')
api.add_resource(Files, root+'/users/<string:email>/files')
api.add_resource(File, root+'/users/<string:email>/files/<int:file>')

#############################################################################
if __name__ == "__main__":

	if(settings.APP_HOST != 'tyeshutty.tk'):
		context = ('cert.pem', 'key.pem')
		app.run(host=settings.APP_HOST, 
			port=settings.APP_PORT, 
			ssl_context=context,
			debug=settings.APP_DEBUG)
	else:
		app.run(debug=settings.APP_DEBUG)
