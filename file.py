from flask import Flask, jsonify, abort, request, make_response, safe_join, send_file, session
from flask_restful import Resource, Api, reqparse
from flask_session import Session
from helpers import check_if_admin
import json
import os
import pymysql.cursors
import settings # Our server and db settings, stored in settings.py
import ssl #include ssl libraries
import sys
#/users/<string:email>
class File(Resource):
# curl -i -H "Content-Type: application/json" -X GET -c cookie-jar -b cookie-jar -k "https://cs3103.cs.unb.ca:5045/users/tshutty@unb.ca/files/4?stream=false"
    def get(self, email, file):
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

        stream = request.args.get('stream', 'false')
        print("pre db")
        dbConnection = pymysql.connect(
            host = settings.MYSQL_HOST,
            user = settings.MYSQL_USER,
            passwd = settings.MYSQL_PASSWD,
            db = settings.MYSQL_DB,
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
        print("post db",row)
        if row is None:
            return make_response(jsonify({'status': 'no folder'}), 404)
        if(row['owner_email'] == session['email'] or session['admin_status'] == 1):
            print("pre stream")
            if stream == 'true':
                filepath = safe_join(settings.UPLOAD_FOLDER, str(row["file_id"]))
                response = send_file(
                    filename_or_fp=filepath,
                    mimetype="application/octet-stream",
                    as_attachment=True,
                    attachment_filename=row["file_name"]
                )
                print("sending stream")
                return response
            else:
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

        print("fetch req=",request)
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
            host = settings.MYSQL_HOST,
            user = settings.MYSQL_USER,
            passwd = settings.MYSQL_PASSWD,
            db = settings.MYSQL_DB,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)
        # First check if parent folder is valid

        sql = 'getFile'
        try:
            cursor = dbConnection.cursor()
            cursor.callproc(sql, [file]) # stored procedure, arguments
            row = cursor.fetchone()
            dbConnection.commit()
        except:
            abort(500) # Nondescript server error
        finally:
            cursor.close()
        print('fetch row=',row)

        if(row is None):
            dbConnection.close()
            return make_response(jsonify({'status':'No file'}), 404)
        if(row['owner_email'] == session['email']  or session['admin_status'] == 1):
            sql = 'setFile'
            try:
                cursor = dbConnection.cursor()
                print('data=',file, name, description, plays_count, last_played, parent, email)
                cursor.callproc(sql, [file, name, description, plays_count, last_played, parent, email])
                dbConnection.commit() #NEEDED for updates and inserts
            except Exception as e:
                print(e)
                return make_response(jsonify({'status':str(e)}), 200)
            except:
                abort(500) # Nondescript server error
            finally:
                cursor.close()
                dbConnection.close()

            return make_response(jsonify({'status':'file updated'}), 204)
        else:
            dbConnection.close()
            return make_response(jsonify({'status': 'not owner'}), 403)
    # curl -i -H "Content-Type: application/json" -X DELETE -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users/tshutty@unb.ca/files/4
    def delete(self, email, file):
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
        if(row['owner_email'] == session['email']  or session['admin_status'] == 1):
            sql = 'deleteFile'
            try:
                cursor = dbConnection.cursor()
                cursor.callproc(sql, [file])
                dbConnection.commit() #NEEDED for updates and inserts
            except Exception as e:
                print(e)
                return make_response(jsonify({'status':'file not deleted'}), 400)
            except:
                abort(500) # Nondescript server error
            finally:
                cursor.close()
                dbConnection.close()

            if os.path.exists(safe_join(settings.UPLOAD_FOLDER, str(file))):
                os.remove(safe_join(settings.UPLOAD_FOLDER, str(file)))

            return make_response(jsonify({'status':'deleted '+str(file)}), 204)
        else:
            dbConnection.close()
            return make_response(jsonify({'status': 'not owner'}), 403)
