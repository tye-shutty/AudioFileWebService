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
class User(Resource):
    #curl -i -H "Content-Type: application/json" -X GET -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users/tshutty@unb.ca
    def get(self, email):
        if(settings.APP_HOST == '127.0.0.1'):
        #     with open('session.json') as f:
        #         session = json.load(f)
            session = settings.SESSION
        else:
            from flask import session
        print('em=',email)
        if 'email' not in session:
            return make_response(jsonify({'status': 'not logged in'}), 403)
            
        check_if_admin()
        if session['email'] != email and session['admin_status'] == 0:
            return make_response(jsonify({'status': 'not logged in as '+email+' and not admin'}), 403)

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
        except:
            abort(500) # Nondescript server error
        finally:
            cursor.close()
            dbConnection.close()
        if row is None:
            return make_response(jsonify({'status': 'no user'}), 404)
        return make_response(jsonify({'user': {'email': row['email'], 'admin_status': row['admin_status']}}), 200) # turn set into json and return it
    #Change email
    # curl -i -H "Content-Type: application/json" -X PATCH -d '{"email":"dum@poopie"}' -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users/tshutty@unb.ca
    #Change email back:
    # curl -i -H "Content-Type: application/json" -X PATCH -d '{"email":"tshutty@unb.ca"}' -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users/dum@poopie
    def patch(self, email):
        if(settings.APP_HOST == '127.0.0.1'):
        #     with open('session.json') as f:
        #         session = json.load(f)
            session = settings.SESSION
        else:
            from flask import session

        if 'email' not in session:
            return make_response(jsonify({'status': 'not logged in'}), 403)
            
        check_if_admin()
        if session['email'] != email and session['admin_status'] == 0:
            return make_response(jsonify({'status': 'not logged in as '+email+' and not admin'}), 403)

        if not request.json or not 'email' in request.json:
            return make_response(jsonify({'status': 'no request'}), 400)

        new_email = request.json['email'].lower()

        dbConnection = pymysql.connect(
            host = settings.MYSQL_HOST,
            user = settings.MYSQL_USER,
            passwd = settings.MYSQL_PASSWD,
            db = settings.MYSQL_DB,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)

        sql = 'setUser'
        try:
            cursor = dbConnection.cursor()
            cursor.callproc(sql, [email, new_email, session['admin_status']])
            dbConnection.commit() #NEEDED for updates and inserts
        except pymysql.err.InternalError as e:
            if email != new_email:
                # print(e)
                return make_response(jsonify({'status':new_email+' in use or '+email+' not in use'}), 400)
            return make_response(jsonify({'status':'no change to '+email}), 200)
        except:
            abort(500) # Nondescript server error
        finally:
            cursor.close()
            dbConnection.close()

        if email == session['email']:
            session['email'] = new_email
        return make_response(jsonify({'status':'changed '+email+' to '+new_email}), 204)
    # curl -i -H "Content-Type: application/json" -X DELETE -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users/tshutty@unb.ca
    def delete(self, email):
        if(settings.APP_HOST == '127.0.0.1'):
        #     with open('session.json') as f:
        #         session = json.load(f)
            session = settings.SESSION
        else:
            from flask import session

        if 'email' not in session:
            return make_response(jsonify({'status': 'not logged in'}), 403)
            
        check_if_admin()
        if session['email'] != email and session['admin_status'] == 0:
            return make_response(jsonify({'status': 'not logged in as '+email+' and not admin'}), 403)

        dbConnection = pymysql.connect(
            host = settings.MYSQL_HOST,
            user = settings.MYSQL_USER,
            passwd = settings.MYSQL_PASSWD,
            db = settings.MYSQL_DB,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)

        sql = 'deleteUser'
        try:
            cursor = dbConnection.cursor()
            cursor.callproc(sql, [email])
            dbConnection.commit() #NEEDED for updates and inserts
        except pymysql.err.InternalError as e:
            return make_response(jsonify({'status':email+' not found'}), 200)
        except:
            abort(500) # Nondescript server error
        finally:
            cursor.close()
            dbConnection.close()

        if email == session['email']:
            session.pop('email',None)
            session.pop('admin_status',None)

        return make_response(jsonify({'status':'deleted '+email}), 200)
