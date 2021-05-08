from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import Resource, Api, reqparse
from flask_session import Session
from helpers import check_if_admin, allowed_file
import json
import os
import pymysql.cursors
import settings # Our server and db settings, stored in settings.py
import ssl #include ssl libraries
import sys
import werkzeug

class Files(Resource):
    # curl -i -H "Content-Type: application/json" -X GET -c cookie-jar -b cookie-jar -k "https://cs3103.cs.unb.ca:5045/users/tshutty@unb.ca/files?string=%"
    def get(self, email):
        if(settings.APP_HOST == '127.0.0.1'):
        #     with open('session.json') as f:
        #         session = json.load(f)
            session = settings.SESSION
        else:
            from flask import session
        if 'email' not in session:
            return make_response(jsonify({'status': 'not logged in'}), 403)
        print('sess0=',session)
        check_if_admin()
        # if(settings.APP_HOST == '127.0.0.1'):
        #     with open('session.json') as f:
        #         session = json.load(f)
        print('sess=',session)
        if session['email'] != email and session['admin_status'] == 0:
            return make_response(jsonify({'status': 'not logged in as '+email+' and not admin'}), 403)

        print(request)
        string = request.args.get('string', "%")

        dbConnection = pymysql.connect(
            host = settings.MYSQL_HOST,
            user = settings.MYSQL_USER,
            passwd = settings.MYSQL_PASSWD,
            db = settings.MYSQL_DB,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)

        sql = 'findFileString'
        try:
            cursor = dbConnection.cursor()
            cursor.callproc(sql, [email,string])
            rows = cursor.fetchall() # get all the results
        except:
            abort(500) # Nondescript server error
        finally:
            cursor.close()
            dbConnection.close()
        return make_response(jsonify({'files': rows}), 200) # turn set into json and return it

    def post(self, email):
        # signin
        # curl -i -H "Content-Type: application/json" -X POST -d '{"username": "tshutty", "password": "..."}' -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/signin
        # create account
        # curl -i -H "Content-Type: application/json" -X POST -d '{"email": "tshutty"}' -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users
        # create folder
        # curl -i -H "Content-Type: application/json" -X POST -d '{"folder_name": "hotdogs","folder_description":"pink", "parent":0}' -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users/tshutty@unb.ca/folders
        # create file
        # curl -i -X POST --form file_description="5:00" --form parent=4 --form "file=@myfile.txt" -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users/tshutty@unb.ca/files

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

        print('form=',request.form)
        print('file=',request.files['file'])
        if (not request.form
        or not 'file_description' in request.form
        or not 'parent' in request.form
        or not 'file' in request.files 
        or request.files['file'] == ''
        or not allowed_file(request.files['file'].filename)):
            return make_response(jsonify({'status': 'invalid request body'}), 400)


        # file_name = request.form['file_name']
        file_description = request.form['file_description']
        parent = request.form['parent']

        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        audio_file = args['file']
        file_name = audio_file.filename
        print(audio_file)

        # file = request.files['file']
        # print(file)

        # filename = secure_filename(file.filename)
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        dbConnection = pymysql.connect(
            host = settings.MYSQL_HOST,
            user = settings.MYSQL_USER,
            passwd = settings.MYSQL_PASSWD,
            db = settings.MYSQL_DB,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)
       
        sql = 'addFile'
        try:
            cursor = dbConnection.cursor()
            sqlArgs = (file_name, file_description, parent, email) # Must be a collection
            cursor.callproc(sql,sqlArgs) # stored procedure, with arguments
            file_id = cursor.fetchone()
            dbConnection.commit() # database was modified, commit the changes
        except Exception as e:
            print(str(e))
            return make_response(jsonify({'status': str(e)}), 400)
        except:
            abort(500) # Nondescript server error
        finally:
            cursor.close()
            dbConnection.close()
        uri = 'https://'+settings.APP_HOST
        if(settings.APP_HOST != 'tyeshutty.tk'):
            uri = uri +':'+str(settings.APP_PORT)
        uri = uri+'/users/'+email+'/'+str(file_id['LAST_INSERT_ID()'])

        audio_file.save(os.path.join(settings.UPLOAD_FOLDER,str(file_id['LAST_INSERT_ID()'])))

        return make_response(jsonify( { "uri" : uri } ), 201) # successful resource creation

