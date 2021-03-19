#!/usr/bin/env python3
#adapted from Rick's code

from flask import Flask, jsonify, abort, request, make_response
from flask_restful import Resource, Api
import pymysql.cursors
import json

import cgitb
import cgi
import sys
cgitb.enable()

import settings # Our server and db settings, stored in settings.py

app = Flask(__name__, static_url_path='/static')
api = Api(app)


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

api.add_resource(Root,'/')

####################################################################################
#
# schools routing: GET and POST, individual school access
#
class Users(Resource):
    # GET: Return all school resources
	#
	# Example request: curl http://cs3103.cs.unb.ca:5045/users
	def get(self):
		dbConnection = pymysql.connect(
			settings.MYSQL_HOST,
			settings.MYSQL_USER,
			settings.MYSQL_PASSWD,
			settings.MYSQL_DB,
			charset='utf8mb4',
			cursorclass= pymysql.cursors.DictCursor)
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
        # curl -i -X POST -H "Content-Type: application/json" -d '{"email": "12pm@mar19", "admin_status": 0}' http://cs3103.cs.unb.ca:5045/users

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
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		# Look closely, Grasshopper: we just created a new resource, so we're
		# returning the uri to it, based on the return value from the stored procedure.
		# Yes, now would be a good time check out the procedure.
		uri = 'http://'+settings.APP_HOST+':'+str(settings.APP_PORT)
		uri = uri+str(request.url_rule)+'/'+email
		return make_response(jsonify( { "uri" : uri } ), 201) # successful resource creation

# class School(Resource):
#     # GET: Return identified school resource
# 	#
# 	# Example request: curl http://info3103.cs.unb.ca:xxxxx/schools/2
# 	def get(self, schoolId):
# 		try:
# 			dbConnection = pymysql.connect(
				# settings.MYSQL_HOST,
				# settings.MYSQL_USER,
				# settings.MYSQL_PASSWD,
				# settings.MYSQL_DB,
# 				charset='utf8mb4',
# 				cursorclass= pymysql.cursors.DictCursor)
# 			sql = 'getSchoolByID'
# 			cursor = dbConnection.cursor()
# 			sqlArgs = (schoolId,)
# 			cursor.callproc(sql,sqlArgs) # stored procedure, no arguments
# 			row = cursor.fetchone() # get the single result
# 			if row is None:
# 				abort(404)
# 		except:
# 			abort(500) # Nondescript server error
# 		finally:
# 			cursor.close()
# 			dbConnection.close()
# 		return make_response(jsonify({"school": row}), 200) # successful

#     # DELETE: Delete identified school resource
#     #
#     # Example request: curl -X DELETE http://info3103.cs.unb.ca:xxxxx/schools/2
# 	def delete(self, schoolId):
# 		print("SchoolId to delete: "+str(schoolId))
# 		# 1. You need to create the stored procedure in MySQLdb (deleteSchool)
# 		# 2. You need to write the code here to call the stored procedure
# 		# 3. What should/could the response code be? How to return it?
# 		# 4. Anytime you change a database, you ned to commit that change.
# 		#       See the POST example for more
# 		return
####################################################################################
#
# Identify/create endpoints and endpoint objects
#
api = Api(app)
api.add_resource(Users, '/users')
# api.add_resource(School, '/schools/<int:schoolId>')


#############################################################################
# xxxxx= last 5 digits of your studentid. If xxxxx > 65535, subtract 30000
if __name__ == "__main__":
#    app.run(host="info3103.cs.unb.ca", port=xxxx, debug=True)
	app.run(host=settings.APP_HOST, port=settings.APP_PORT, debug=settings.APP_DEBUG)
