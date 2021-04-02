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
class Folder(Resource):
# curl -i -H "Content-Type: application/json" -X GET -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users/tshutty@unb.ca/folders/4
    def get(self, email, folder):
        if(settings.APP_HOST == '127.0.0.1'):
        #     with open('session.json') as f:
        #         session = json.load(f)
            session = settings.SESSION
        else:
            from flask import session
        if 'email' not in session:
            return make_response(jsonify({'status': 'not logged in'}), 403)
            
        check_if_admin()
        # if(settings.APP_HOST == '127.0.0.1'):
        #     with open('session.json') as f:
        #         session = json.load(f)
        if session['email'] != email and session['admin_status'] == 0:
            return make_response(jsonify({'status': 'not logged in as '+email+' and not admin'}), 403)


        dbConnection = pymysql.connect(
            host = settings.MYSQL_HOST,
            user = settings.MYSQL_USER,
            passwd = settings.MYSQL_PASSWD,
            db = settings.MYSQL_DB,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)

        sql = 'getFolder'
        try:
            cursor = dbConnection.cursor()
            cursor.callproc(sql, [folder]) # stored procedure, arguments
            row = cursor.fetchone()
        except:
            abort(500) # Nondescript server error
        finally:
            cursor.close()
            dbConnection.close()
        print(row)
        if row is None:
            return make_response(jsonify({'status': 'no folder'}), 404)
        elif(row['owner_email'] == session['email'] or session['admin_status'] == 1):
            return make_response(jsonify({'folder': row}), 200) # turn set into json and return it
        else:
            return make_response(jsonify({'status': 'not owner'}), 403)


    # curl -i -H "Content-Type: application/json" -X PATCH -d '{"name":"nice","description":"blue"}' -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users/tshutty@unb.ca/folders/4
    def patch(self, email, folder):
        if(settings.APP_HOST == '127.0.0.1'):
        #     with open('session.json') as f:
        #         session = json.load(f)
            session = settings.SESSION
        else:
            from flask import session

        if 'email' not in session:
            return make_response(jsonify({'status': 'not logged in'}), 403)
            
        check_if_admin()
        # if(settings.APP_HOST == '127.0.0.1'):
        #     with open('session.json') as f:
        #         session = json.load(f)
        if session['email'] != email and session['admin_status'] == 0:
            return make_response(jsonify({'status': 'not logged in as '+email+' and not admin'}), 403)

        if (not request.json or not 'name' in request.json or not 'description' in request.json):
            return make_response(jsonify({'status': 'no request'}), 400)

        name = request.json['name']
        description = request.json['description']

        dbConnection = pymysql.connect(
            host = settings.MYSQL_HOST,
            user = settings.MYSQL_USER,
            passwd = settings.MYSQL_PASSWD,
            db = settings.MYSQL_DB,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)

        sql = 'getFolder'
        try:
            cursor = dbConnection.cursor()
            cursor.callproc(sql, [folder]) # stored procedure, arguments
            row = cursor.fetchone()
        except:
            abort(500) # Nondescript server error
        finally:
            cursor.close()
        print(row)

        if row is None:
            return make_response(jsonify({'status': 'no folder'}), 404)
        if(row['owner_email'] == session['email'] or session['admin_status'] == 1):
            sql = 'setFolder'
            try:
                cursor = dbConnection.cursor()
                cursor.callproc(sql, [folder, name, description])
                dbConnection.commit() #NEEDED for updates and inserts
            except pymysql.err.InternalError as e:
                return make_response(jsonify({'status':str(e)}), 200)
            except:
                abort(500) # Nondescript server error
            finally:
                cursor.close()
                dbConnection.close()

            return make_response(jsonify({'status':'folder updated'}), 204)
        else:
            dbConnection.close()
            return make_response(jsonify({'status': 'not owner and not admin'}), 403)
    # curl -i -H "Content-Type: application/json" -X DELETE -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users/tshutty@unb.ca/folders/4
    def delete(self, email, folder):
        if(settings.APP_HOST == '127.0.0.1'):
        #     with open('session.json') as f:
        #         session = json.load(f)
            session = settings.SESSION
            print("sess=",session)
        else:
            from flask import session

        if 'email' not in session:
            return make_response(jsonify({'status': 'not logged in'}), 403)
            
        check_if_admin()
        # if(settings.APP_HOST == '127.0.0.1'):
        #     with open('session.json') as f:
        #         session = json.load(f)
        if session['email'] != email and session['admin_status'] == 0:
            return make_response(jsonify({'status': 'not logged in as '+email+' and not admin'}), 403)

        dbConnection = pymysql.connect(
            host = settings.MYSQL_HOST,
            user = settings.MYSQL_USER,
            passwd = settings.MYSQL_PASSWD,
            db = settings.MYSQL_DB,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)
        
        sql = 'getFolder'
        try:
            cursor = dbConnection.cursor()
            cursor.callproc(sql, [folder]) # stored procedure, arguments
            row = cursor.fetchone()
        except:
            abort(500) # Nondescript server error
        finally:
            cursor.close()
        print(row)
        if(row is None):
            dbConnection.close()
            return make_response(jsonify({'status':'No folder'}), 200)
        
        print('as=',session['admin_status'])
        if(row['owner_email'] == session['email'] or session['admin_status'] == 1):
            sql = 'deleteFolder'
            try:
                cursor = dbConnection.cursor()
                cursor.callproc(sql, [folder])
                dbConnection.commit() #NEEDED for updates and inserts
            except pymysql.err.InternalError as e:
                print(e)
                return make_response(jsonify({'status':'folder not deleted'}), 400)
            except:
                abort(500) # Nondescript server error
            finally:
                cursor.close()
                dbConnection.close()

            return make_response(jsonify({'status':'deleted '+str(folder)}), 200)
        else:
            dbConnection.close()
            return make_response(jsonify({'status': 'not owner'}), 403)
