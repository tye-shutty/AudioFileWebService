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
# curl -i -H "Content-Type: application/json" -X GET -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users/tshutty@unb.ca/files/4
class File(Resource):
    def get(self, email, file):
        if 'email' not in session:
            return make_response(jsonify({'status': 'not logged in'}), 403)
            
        check_if_admin()
        if session['email'] != email and session['admin_status'] == 0:
            return make_response(jsonify({'status': 'not logged in as '+email+' and not admin'}), 403)

        dbConnection = pymysql.connect(
            settings.MYSQL_HOST,
            settings.MYSQL_USER,
            settings.MYSQL_PASSWD,
            settings.MYSQL_DB,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)

        sql = 'getFile'
        try:
            cursor = dbConnection.cursor()
            cursor.callproc(sql, [file]) # stored procedure, arguments
            row = cursor.fetchone()
        except:
            abort(500) # Nondescript server error
        finally:
            cursor.close()
            dbConnection.close()
        print(row)
        if(row is not None and row['owner_email'] == session['email']):
            return make_response(jsonify({'file': row}), 200) # turn set into json and return it
        else:
            return make_response(jsonify({'status': 'not owner'}), 403)


    # signin
    # curl -i -H "Content-Type: application/json" -X POST -d '{"username": "tshutty", "password": "..."}' -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/signin
    # create account
    # curl -i -H "Content-Type: application/json" -X POST -d '{"email": "tshutty"}' -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users
    # create folder
    # curl -i -H "Content-Type: application/json" -X POST -d '{"folder_name": "hotdogs","folder_description":"pink", "parent":0}' -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users/tshutty@unb.ca/folders
    # create file
    # curl -i -H "Content-Type: application/json" -X POST -d '{"file_name": "jill.wav","file_description":"5:00", "parent":4}' -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users/tshutty@unb.ca/files
    # create subfolder
    # curl -i -H "Content-Type: application/json" -X POST -d '{"folder_name": "hotdogs","folder_description":"purple","parent":4}' -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users/tshutty@unb.ca/folders
    # patch file
    # curl -i -H "Content-Type: application/json" -X PATCH -d '{"name":"song2.mp3","description":"Blur","plays_count":3000,"last_played":"2021-03-26 18:32:48","parent":5}' -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users/tshutty@unb.ca/files/4
    def patch(self, email, file):

        if 'email' not in session:
            return make_response(jsonify({'status': 'not logged in'}), 403)
            
        check_if_admin()
        if session['email'] != email and session['admin_status'] == 0:
            return make_response(jsonify({'status': 'not logged in as '+email+' and not admin'}), 403)

        if (not request.json or not 'name' in request.json
        or not 'description' in request.json
        or not 'plays_count' in request.json
        or not 'last_played' in request.json
        or not 'parent' in request.json):
            return make_response(jsonify({'status': 'no request'}), 400)

        name = request.json['name']
        description = request.json['description']
        plays_count = request.json['plays_count']
        last_played = request.json['last_played']
        parent = request.json['parent']

        dbConnection = pymysql.connect(
            settings.MYSQL_HOST,
            settings.MYSQL_USER,
            settings.MYSQL_PASSWD,
            settings.MYSQL_DB,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)
        # First check if parent folder is valid

        sql = 'getFile'
        try:
            cursor = dbConnection.cursor()
            cursor.callproc(sql, [file]) # stored procedure, arguments
            row = cursor.fetchone()
        except:
            abort(500) # Nondescript server error
        finally:
            cursor.close()
        print(row)

        if(row is not None and row['owner_email'] == session['email']):
            sql = 'setFile'
            try:
                cursor = dbConnection.cursor()
                cursor.callproc(sql, [file, name, description, plays_count, last_played, parent])
                dbConnection.commit() #NEEDED for updates and inserts
            except pymysql.err.InternalError as e:
                return make_response(jsonify({'status':'no change to '+email}), 200)
            except:
                abort(500) # Nondescript server error
            finally:
                cursor.close()
                dbConnection.close()

            return make_response(jsonify({'status':'file updated'}), 200)
        else:
            dbConnection.close()
            return make_response(jsonify({'status': 'not owner'}), 403)
    # curl -i -H "Content-Type: application/json" -X DELETE -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users/tshutty@unb.ca/files/4
    def delete(self, email, file):

        if 'email' not in session:
            return make_response(jsonify({'status': 'not logged in'}), 403)
            
        check_if_admin()
        if session['email'] != email and session['admin_status'] == 0:
            return make_response(jsonify({'status': 'not logged in as '+email+' and not admin'}), 403)

        dbConnection = pymysql.connect(
            settings.MYSQL_HOST,
            settings.MYSQL_USER,
            settings.MYSQL_PASSWD,
            settings.MYSQL_DB,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)
        
        sql = 'getFile'
        try:
            cursor = dbConnection.cursor()
            cursor.callproc(sql, [file]) # stored procedure, arguments
            row = cursor.fetchone()
        except:
            abort(500) # Nondescript server error
        finally:
            cursor.close()
        print(row)
        if(row is None):
            dbConnection.close()
            return make_response(jsonify({'status':'No file'}), 200)
        if(row['owner_email'] == session['email']):
            sql = 'deleteFile'
            try:
                cursor = dbConnection.cursor()
                cursor.callproc(sql, [file])
                dbConnection.commit() #NEEDED for updates and inserts
            except pymysql.err.InternalError as e:
                print(e)
                return make_response(jsonify({'status':'file not deleted'}), 400)
            except:
                abort(500) # Nondescript server error
            finally:
                cursor.close()
                dbConnection.close()

            return make_response(jsonify({'status':'deleted '+str(file)}), 200)
        else:
            dbConnection.close()
            return make_response(jsonify({'status': 'not owner'}), 403)
