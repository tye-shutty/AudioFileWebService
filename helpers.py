
from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import Resource, Api, reqparse
from flask_session import Session
import json
import pymysql.cursors
import settings # Our server and db settings, stored in settings.py
import ssl #include ssl libraries
import sys

def check_if_admin():

    if(settings.APP_HOST == '127.0.0.1'):
    #     with open('session.json') as f:
    #         session = json.load(f)
        session = settings.SESSION
    else:
        from flask import session
        
    dbConnection = pymysql.connect(
        host = settings.MYSQL_HOST,
        user = settings.MYSQL_USER,
        passwd = settings.MYSQL_PASSWD,
        db = settings.MYSQL_DB,
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

    # if(settings.APP_HOST == '127.0.0.1'):
    #     with open('session.json', 'w') as json_file:
    #         json.dump(session, json_file)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS
