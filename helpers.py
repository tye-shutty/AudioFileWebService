
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

def check_if_admin():
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
			row = cursor.fetchall() # get all the results
			if len(row) == 0:
				return make_response(jsonify({'status': 'no account'}), 403)

			session['admin_status'] = row[0]['admin_status']
		except Exception as e:
			print(e)
			abort(500) # Nondescript server error
		finally:
			cursor.close()
	dbConnection.close()
	print('as=',session['admin_status'])
