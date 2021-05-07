from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import Resource, Api, reqparse
from flask_session import Session
from helpers import check_if_admin
import json
import pymysql.cursors
import settings # Our server and db settings, stored in settings.py
import ssl #include ssl libraries
import sys

class Users(Resource):
    # GET: Only for admins, returns non admins
    # curl -i -H "Content-Type: application/json" -X GET -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users
    def get(self):
        if(settings.APP_HOST == '127.0.0.1'):
        #     with open('session.json') as f:
        #         session = json.load(f)
            session = settings.SESSION
        else:
            from flask import session

        if 'email' not in session:
            return make_response(jsonify({'status': 'not logged in'}), 403)
        
        check_if_admin()
        if session['admin_status'] == 0:
            return make_response(jsonify({'status': 'not admin'}), 403)

        # dbConnection = pymysql.connect(
        #     settings.MYSQL_HOST,
        #     settings.MYSQL_USER,
        #     settings.MYSQL_PASSWD,
        #     settings.MYSQL_DB,
        #     charset='utf8mb4',
        #     cursorclass= pymysql.cursors.DictCursor)

        dbConnection = pymysql.connect(
            host = settings.MYSQL_HOST,
            user = settings.MYSQL_USER,
            passwd = settings.MYSQL_PASSWD,
            db = settings.MYSQL_DB,
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

    #email must match unb email to be able to access restricted resources
    # curl -i -H "Content-Type: application/json" -X POST -d '{"email": "tshutty@unb.ca"}' -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users
    def post(self):
        if(settings.APP_HOST == '127.0.0.1'):
        #     with open('session.json') as f:
        #         session = json.load(f)
            session = settings.SESSION
        else:
            from flask import session
        if not request.json or not 'email' in request.json or not 'password' in request.json:
            return make_response(jsonify({'status': 'no request'}), 400)

        email = request.json['email']
        password = request.json['password']
        print('len=',len(email))
        if len(email) < 1 or len(email) > 200:
            return make_response(jsonify({'status': 'email must be > 1 < 200 char'}), 400)

        dbConnection = pymysql.connect(
            host = settings.MYSQL_HOST,
            user = settings.MYSQL_USER,
            passwd = settings.MYSQL_PASSWD,
            db = settings.MYSQL_DB,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)
        sql = 'addUser'
        try:
            cursor = dbConnection.cursor()
            sqlArgs = (email, password, 0) # Must be a collection
            cursor.callproc(sql,sqlArgs) # stored procedure, with arguments
            # row = cursor.fetchone()
            dbConnection.commit() # database was modified, commit the changes
        except Exception as e:
            code, msg = e.args
            print('sql error', str(e))
            return make_response(jsonify({'status': msg}), 409)
        finally:
            cursor.close()
            dbConnection.close()
        # Look closely, Grasshopper: we just created a new resource, so we're
        # returning the uri to it, based on the return value from the stored procedure.
        # Yes, now would be a good time check out the procedure.
        uri = 'https://'+settings.APP_HOST
        if(settings.APP_HOST != tyeshutty.tk):
            uri = uri +':'+str(settings.APP_PORT)
        uri = uri+str(request.url_rule)+'/'+email
        return make_response(jsonify( { "uri" : uri } ), 201) # successful resource creation
