from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import Resource, Api, reqparse
from flask_session import Session
from helpers import check_if_admin
import json
import pymysql.cursors
import settings # Our server and db settings, stored in settings.py
import ssl #include ssl libraries
import sys
#/users/<string:email>
#curl -i -H "Content-Type: application/json" -X GET -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users/tshutty@unb.ca
class User(Resource):
	def get(self, email):
		if 'email' not in session or session['email'] != email:
			return make_response(jsonify({'status': 'not logged in as '+email}), 403)

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
