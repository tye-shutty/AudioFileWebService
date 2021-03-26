from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import Resource, Api, reqparse
from flask_session import Session
from helpers import check_if_admin
import json
import pymysql.cursors
import settings # Our server and db settings, stored in settings.py
import ssl #include ssl libraries
import sys

class Folders(Resource):
    # curl -i -H "Content-Type: application/json" -X GET -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users
    # def get(self):

    #     if 'email' not in session:
    #         return make_response(jsonify({'status': 'not logged in'}), 403)

    #     dbConnection = pymysql.connect(
    #         settings.MYSQL_HOST,
    #         settings.MYSQL_USER,
    #         settings.MYSQL_PASSWD,
    #         settings.MYSQL_DB,
    #         charset='utf8mb4',
    #         cursorclass= pymysql.cursors.DictCursor)

    #     sql = 'getUser'
    #     try:
    #         cursor = dbConnection.cursor()
    #         cursor.callproc(sql, [session['email']]) # stored procedure, arguments
    #         user = cursor.fetchone()
    #     except:
    #         abort(500) # Nondescript server error
    #     finally:
    #         cursor.close()
    #         # dbConnection.close()
    #     print('user=',user)
    #     sql = 'getFolders'
    #     try:
    #         cursor = dbConnection.cursor()
    #         cursor.callproc(sql, [user['root']]) # stored procedure, no arguments
    #         rows = cursor.fetchall() # get all the results
    #     except:
    #         abort(500) # Nondescript server error
    #     finally:
    #         cursor.close()
    #         dbConnection.close()
    #     return make_response(jsonify({'folders': rows}), 200) # turn set into json and return it

    def post(self, email):
        # signin
        # curl -i -H "Content-Type: application/json" -X POST -d '{"username": "tshutty", "password": "..."}' -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/signin
        # create account
        # curl -i -H "Content-Type: application/json" -X POST -d '{"email": "tshutty"}' -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users
        # create folder
        # curl -i -H "Content-Type: application/json" -X POST -d '{"folder_name": "hotdogs","folder_description":"pink"}' -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users/tshutty@unb.ca/folders
        # create subfolder
        # curl -i -H "Content-Type: application/json" -X POST -d '{"folder_name": "hotdogs","folder_description":"purple","parent":4}' -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users/tshutty@unb.ca/folders
        

        if 'email' not in session:
            return make_response(jsonify({'status': 'not logged in'}), 403)

        if (not request.json or not 'folder_name' in request.json or not 'folder_description' in request.json):
            return make_response(jsonify({'status': 'invalid request body'}), 400)

        folder_name = request.json['folder_name']
        folder_description = request.json['folder_description']
        parent = request.json['parent']

        dbConnection = pymysql.connect(settings.MYSQL_HOST,
            settings.MYSQL_USER,
            settings.MYSQL_PASSWD,
            settings.MYSQL_DB,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)
       
        sql = 'addFolder'
        try:
            cursor = dbConnection.cursor()
            sqlArgs = (folder_name, folder_description, parent, session['email']) # Must be a collection
            cursor.callproc(sql,sqlArgs) # stored procedure, with arguments
            folder_id = cursor.fetchone()
            dbConnection.commit() # database was modified, commit the changes
        except pymysql.err.InternalError:
            return make_response(jsonify({'status': 'no such owned parent folder'}), 400)
        except:
            abort(500) # Nondescript server error
        finally:
            cursor.close()
            dbConnection.close()
        print('folder_id=',folder_id)
        
        uri = 'https://'+settings.APP_HOST+':'+str(settings.APP_PORT)
        uri = uri+str(request.url_rule)+'/'+str(folder_id['LAST_INSERT_ID()'])
        return make_response(jsonify( { "uri" : uri } ), 201) # successful resource creation

