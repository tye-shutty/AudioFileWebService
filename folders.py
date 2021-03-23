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
        # curl -i -H "Content-Type: application/json" -X POST -d '{"email": "mar20@2:19pm"}' -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users

        if 'email' not in session:
            return make_response(jsonify({'status': 'not logged in'}), 403)

        if (not request.json or not 'folder_name' in request.json
        or not 'folder_description' in request.json
        or not 'parent' in request.json):
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
        sql = 'findFolderOwner'
        try:
            cursor = dbConnection.cursor()
            cursor.callproc(sql,[parent]) # stored procedure, with arguments
            owner = cursor.fetchone()
        except pymysql.err.InternalError:
            return make_response(jsonify({'status': 'no such parent folder'}), 400)
        except:
            abort(500) # Nondescript server error
        finally:
            cursor.close()
        print('owner=',owner)
        if(owner == session['email']):
            sql = 'addFolder'
            try:
                cursor = dbConnection.cursor()
                sqlArgs = (folder_name, folder_description, parent) # Must be a collection
                cursor.callproc(sql,sqlArgs) # stored procedure, with arguments
                folder_id = cursor.fetchone()
                dbConnection.commit() # database was modified, commit the changes
            except pymysql.err.InternalError:
                return make_response(jsonify({'status': 'no such parent folder'}), 400)
            except:
                abort(500) # Nondescript server error
            finally:
                cursor.close()
                dbConnection.close()
            print('folder_id=',folder_id)
        # Look closely, Grasshopper: we just created a new resource, so we're
        # returning the uri to it, based on the return value from the stored procedure.
        # Yes, now would be a good time check out the procedure.
            uri = 'https://'+settings.APP_HOST+':'+str(settings.APP_PORT)
            uri = uri+str(request.url_rule)+'/'+str(folder_id)
            return make_response(jsonify( { "uri" : uri } ), 201) # successful resource creation
        else:
            return make_response(jsonify({'status': 'not owner'}), 403)
            dbConnection.close()
