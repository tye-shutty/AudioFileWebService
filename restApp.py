#!/usr/bin/env python3
#adapted from Rick's code
from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import Resource, Api, reqparse
from flask_session import Session
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
#
class Root(Resource):
   # get method. What might others be aptly named? (hint: post)
	def get(self):
		return app.send_static_file('index.html')

####################################################################################
#
# schools routing: GET and POST, individual school access
#
class SignIn(Resource):
	#
	# Set Session and return Cookie
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X POST -d '{"email": "Casper", "password": "crap"}'
	#  	-c cookie-jar -k https://cs3103.cs.unb.ca:61340/signin
	#
	def post(self):
		print('initial data\nsid=',session.sid,'session=',session)
		print('cookie=', request.cookies)
		# print('request=', request.headers)

		if not request.json:
			abort(400) # bad request

		# Parse the json
		parser = reqparse.RequestParser()
		try:
 			# Check for required attributes in json document, create a dictionary
			parser.add_argument('username', type=str, required=True)
			parser.add_argument('password', type=str, required=True)
			request_params = parser.parse_args()
			print('rp=', request_params)
		except:
			abort(400) # bad request

		if 'email' in session:
			response = {'status': 'success'}
			responseCode = 200
		else:
			try:
				ldapServer = Server(host=settings.LDAP_HOST)
				ldapConnection = Connection(ldapServer,
					raise_exceptions=True,
					user='uid='+request_params['username']+', ou=People,ou=fcs,o=unb',
					password = request_params['password'])
				ldapConnection.open()
				ldapConnection.start_tls()
				ldapConnection.bind()
				# At this point we have sucessfully authenticated.
				session['email'] = request_params['username']+'@unb.ca'
				response = {'status': 'success' }
				responseCode = 201
			except LDAPException:
				response = {'status': 'Access denied'}
				responseCode = 403
			finally:
				ldapConnection.unbind()

		return make_response(jsonify(response), responseCode)

	# GET: Check Cookie data with Session data
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar
	#	-k https://cs3103.cs.unb.ca:61340/signin
	def get(self):
		success = False
		if 'email' in session:
			response = {'status': 'success'}
			responseCode = 200
		else:
			response = {'status': 'not logged in'}
			responseCode = 403

		return make_response(jsonify(response), responseCode)

	# DELETE: Check Cookie data with Session data
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar
	#	-k https://info3103.cs.unb.ca:61340/signin

	def delete(self):
		# print('sid=',session.sid,'session=',session)
		if 'email' in session:
			session.pop('email',None)

		response = {'status': 'success'}
		responseCode = 200
		return make_response(jsonify(response), responseCode)


class Users(Resource):
    # GET: Only for admins
	#
	# Example request: curl http://cs3103.cs.unb.ca:5045/users
	def get(self):

		if 'email' not in session:
			return make_response(jsonify({'status': 'not logged in'}), 403)

		dbConnection = pymysql.connect(
			settings.MYSQL_HOST,
			settings.MYSQL_USER,
			settings.MYSQL_PASSWD,
			settings.MYSQL_DB,
			charset='utf8mb4',
			cursorclass= pymysql.cursors.DictCursor)
			
		if 'admin_status' not in session:
			sql = 'getUser'
			try:
				cursor = dbConnection.cursor()
				cursor.callproc(sql, [session['email']]) # stored procedure, arguments
				rows = cursor.fetchall() # get all the results
				if len(rows) == 0:
					return make_response(jsonify({'status': 'no account'}), 403)

				session['admin_status'] = rows[0]['admin_status']
			except Exception as e:
				print(e)
				abort(500) # Nondescript server error
			finally:
				cursor.close()
				dbConnection.close()

		if session['admin_status'] == 0:
			return make_response(jsonify({'status': 'not an admin'}), 403)

		sql = 'getUsers'
		try:
			cursor = dbConnection.cursor()
			cursor.callproc(sql) # stored procedure, no arguments
			rows = cursor.fetchall() # get all the results
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify({'users': rows}), 200) # turn set into json and return it

	def post(self):
        #
        # Sample command line usage:
        #
        # curl -i -X POST -H "Content-Type: application/json" -d '{"email": "12pm@mar19"}' http://cs3103.cs.unb.ca:5045/users

		if not request.json or not 'email' in request.json:
			abort(400) # bad request

			# The request object holds the ... wait for it ... client request!
		# Pull the results out of the json request
		email = request.json['email']

		dbConnection = pymysql.connect(settings.MYSQL_HOST,
			settings.MYSQL_USER,
			settings.MYSQL_PASSWD,
			settings.MYSQL_DB,
			charset='utf8mb4',
			cursorclass= pymysql.cursors.DictCursor)
		sql = 'addUser'
		try:
			cursor = dbConnection.cursor()
			sqlArgs = (email, 1) # Must be a collection
			cursor.callproc(sql,sqlArgs) # stored procedure, with arguments
			row = cursor.fetchone()
			dbConnection.commit() # database was modified, commit the changes
		except pymysql.err.IntegrityError:
			return make_response(jsonify({'status': 'account exists'}), 409)

		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		# Look closely, Grasshopper: we just created a new resource, so we're
		# returning the uri to it, based on the return value from the stored procedure.
		# Yes, now would be a good time check out the procedure.
		uri = 'https://'+settings.APP_HOST+':'+str(settings.APP_PORT)
		uri = uri+str(request.url_rule)+'/'+email
		return make_response(jsonify( { "uri" : uri } ), 201) # successful resource creation

class User(Resource):
	def get(self):
		if 'email' not in session:
			return make_response(jsonify({'status': 'not logged in'}), 403)

		dbConnection = pymysql.connect(
			settings.MYSQL_HOST,
			settings.MYSQL_USER,
			settings.MYSQL_PASSWD,
			settings.MYSQL_DB,
			charset='utf8mb4',
			cursorclass= pymysql.cursors.DictCursor)

		sql = 'getUser'
		try:
			cursor = dbConnection.cursor()
			cursor.callproc(sql, [session['email']]) # stored procedure, arguments
			row = cursor.fetchone()
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify({'user': row}), 200) # turn set into json and return it

#
# Identify/create endpoints and endpoint objects
api = Api(app)
api.add_resource(Root,'/')
api.add_resource(SignIn, '/signin')
api.add_resource(Users, '/users')
api.add_resource(User, '/users/<string:email>')


#############################################################################
# xxxxx= last 5 digits of your studentid. If xxxxx > 65535, subtract 30000
if __name__ == "__main__":
#    app.run(host="info3103.cs.unb.ca", port=xxxx, debug=True)
	context = ('cert.pem', 'key.pem') # Identify the certificates you've generated.
	app.run(host=settings.APP_HOST, 
		port=settings.APP_PORT, 
		ssl_context=context,
		debug=settings.APP_DEBUG)
