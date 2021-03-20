from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import Resource, Api, reqparse
from flask_session import Session
from helpers import check_if_admin
import json
import pymysql.cursors
import settings # Our server and db settings, stored in settings.py
import ssl #include ssl libraries
import sys

# /users/{email}/authorize
# curl -i -H "Content-Type: application/json" -X PATCH -d '{"admin_status": 0}' -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users/tshutty@unb.ca/authorize
class Authorize(Resource):
	def patch(self, email):
		if 'email' not in session:
			return make_response(jsonify({'status': 'not logged in'}), 403)

		check_if_admin()
		if session['admin_status'] == 0:
			return make_response(jsonify({'status': 'not admin'}), 403)
			
		if not request.json or not 'admin_status' in request.json:
			return make_response(jsonify({'status': 'no request data'}), 400)

		new_admin_status = request.json['admin_status']
		print(new_admin_status, type(new_admin_status), email)
		dbConnection = pymysql.connect(
			settings.MYSQL_HOST,
			settings.MYSQL_USER,
			settings.MYSQL_PASSWD,
			settings.MYSQL_DB,
			charset='utf8mb4',
			cursorclass= pymysql.cursors.DictCursor)

		sql = 'setAdmin'
		try:
			cursor = dbConnection.cursor()
			cursor.callproc(sql, [email, new_admin_status])
			dbConnection.commit() #NEEDED for updates and inserts
		except pymysql.err.InternalError:
			return make_response(jsonify({'status':'no change to '+email}), 200)
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify({'status':'updated '+email}), 200)
