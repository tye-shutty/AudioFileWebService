
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

class SignIn(Resource):
	#curl -i -H "Content-Type: application/json" -X POST -d '{"username": "tshutty", "password": "..."}' -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/signin
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
	# curl -i -H "Content-Type: application/json" -X GET -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/signin
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
	# curl -i -H "Content-Type: application/json" -X DELETE -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/signin

	def delete(self):
		# print('sid=',session.sid,'session=',session)
		if 'email' in session:
			session.pop('email',None)
			session.pop('admin_status',None)
		print('del sess=',session)
		response = {'status': 'success'}
		responseCode = 200
		return make_response(jsonify(response), responseCode)
