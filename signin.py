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
    # curl -i -H "Content-Type: application/json" -X POST -d '{"username": "tshutty", "password": "..."}' -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/signin
    
    def post(self):
        if(settings.APP_HOST == '127.0.0.1'):
            # with open('session.json') as f:
            #     session = json.load(f)
            session = settings.SESSION
        else:
            from flask import session

        print('initial data=',session)
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

        if 'email' in session and session['email'] == request_params['username']+'@unb.ca':
            response = {'status': 'success'}
            responseCode = 200
        else:
            try:
                if(settings.APP_HOST == 'cs3103.cs.unb.ca' and
                request_params['username'] != 'admin'):    # temporary access to demo admin
                    print('signing in with UNB')
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
                print('sess email=',session['email'])
                response = {'status': 'success' }
                responseCode = 201
            except LDAPException:
                response = {'status': 'Access denied'}
                responseCode = 403
            finally:
                if(settings.APP_HOST != '127.0.0.1' and
                request_params['username'] != 'admin'):    # temporary access to demo admin
                    ldapConnection.unbind()
        resp = make_response(jsonify(response), responseCode)
        # resp.set_cookie('cookie_key', value="cookie_value", domain='127.0.0.1')
        # if(settings.APP_HOST == '127.0.0.1'):
        #     with open('session.json', 'w') as json_file:
        #         json.dump(session, json_file)
        return resp

    # GET: Check Cookie data with Session data
    #
    # curl -i -H "Content-Type: application/json" -X GET -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/signin
    def get(self):
        if(settings.APP_HOST == '127.0.0.1'):
            # with open('session.json') as f:
            #     session = json.load(f)
            session = settings.SESSION
        else:
            from flask import session
        print('sess=',session)
        success = False
        if 'email' in session:
            response = {'status': session['email']}
            responseCode = 200
        else:
            response = {'status': 'not logged in'}
            responseCode = 403

        return make_response(jsonify(response), responseCode)

    # DELETE: Check Cookie data with Session data
    #
    # curl -i -H "Content-Type: application/json" -X DELETE -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/signin
    def delete(self):
        if(settings.APP_HOST == '127.0.0.1'):
            # with open('session.json') as f:
            #     session = json.load(f)
            session = settings.SESSION
        else:
            from flask import session
        print('sid=',session.sid,'session=',session)
        if 'email' in session:
            session.pop('email',None)
            session.pop('admin_status',None)
        print('del sess=',session)
        response = {'status': 'success'}
        responseCode = 200

        # if(settings.APP_HOST == '127.0.0.1'):
        #     with open('session.json', 'w') as json_file:
        #         json.dump(session, json_file)
        return make_response(jsonify(response), responseCode)
