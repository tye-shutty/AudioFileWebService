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
import traceback


class SignIn(Resource):
    # curl -i -H "Content-Type: application/json" -X POST -d '{"email": "tshutty", "password": "..."}' -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/signin
    
    def post(self):
        if(settings.APP_HOST == '127.0.0.1'):
            # with open('session.json') as f:
            #     session = json.load(f)
            session = settings.SESSION
        else:
            from flask import session

        print('initial data=',settings.APP_HOST, session)
        print('cookie=', request.cookies)
        # print('request=', request.headers)

        if not request.json:
            print('no req')
            abort(400) # bad request

        # Parse the json
        parser = reqparse.RequestParser()
        try:
             # Check for required attributes in json document, create a dictionary
            parser.add_argument('email', type=str, required=True)
            parser.add_argument('password', type=str, required=True)
            request_params = parser.parse_args()
            print('rp=', request_params)
            if(settings.APP_HOST == 'cs3103.cs.unb.ca'):
                email = request_params['email']+'@unb.ca'
            else:
                email = request_params['email'] #TODO: confirm if valid email
        except:
            print('bad req=',request.json)
            abort(400) # bad request
        #need to be able to prerun code on the front end on page reload to take advantage of this feature
        # if 'email' in session and session['email'] == email:
        #     response = {'status': 'success'}
        #     responseCode = 200
        # else:
        try:
            if(settings.APP_HOST == 'cs3103.cs.unb.ca'):    # temporary access to demo admin: and
            # request_params['email'] != 'admin'
                print('signing in with UNB')
                ldapServer = Server(host=settings.LDAP_HOST)
                ldapConnection = Connection(ldapServer,
                    raise_exceptions=True,
                    user='uid='+request_params['email']+', ou=People,ou=fcs,o=unb',
                    password = request_params['password'])
                ldapConnection.open()
                ldapConnection.start_tls()
                ldapConnection.bind()
            else:
                print('singin in with db')
                dbConnection = pymysql.connect(
                    host = settings.MYSQL_HOST,
                    user = settings.MYSQL_USER,
                    passwd = settings.MYSQL_PASSWD,
                    db = settings.MYSQL_DB,
                    charset='utf8mb4',
                    cursorclass= pymysql.cursors.DictCursor)

                sql = 'getUser'
                try:
                    cursor = dbConnection.cursor()
                    cursor.callproc(sql, [email]) # stored procedure, arguments
                    row = cursor.fetchone()
                    # print('row=', row)
                    if(row == None):
                        return make_response(jsonify({'status': 'No account'}), 403)
                    elif(row['pswd'] != request_params['password']):
                        return make_response(jsonify({'status': 'Access denied'}), 403)
                except Exception as e:
                    print('exception', e)
                    traceback.print_exc()
                    return make_response(jsonify({'status': str(e)}), 400)
                finally:
                    cursor.close()
                    dbConnection.close()
                print('row=', row)
                    
            # At this point we have sucessfully authenticated.
            session['email'] = email
            print('sess email=',session['email'])
            response = {'status': 'success' }
            responseCode = 201
        except LDAPException:
            response = {'status': 'Access denied'}
            responseCode = 403
        finally:
            if(settings.APP_HOST == 'cs3103.cs.unb.ca' and
            request_params['email'] != 'admin'):    # temporary access to demo admin
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
            print('session=', session)
        else:
            from flask import session
        print('session=',session)
        if 'email' in session:
            session.pop('email',None)
            session.pop('admin_status',None)
        print('del sess=',session)
        response = {'status': 'success, session='+str(session)}
        responseCode = 200

        # if(settings.APP_HOST == '127.0.0.1'):
        #     with open('session.json', 'w') as json_file:
        #         json.dump(session, json_file)
        return make_response(jsonify(response), responseCode)
