#/usr/bin/env python3
APP_HOST = 'cs3103.cs.unb.ca'
#'ec2-18-218-32-161.us-east-2.compute.amazonaws.com' #'127.0.0.1' #'cs3103.cs.unb.ca'
APP_PORT =  8027 #5045
APP_DEBUG = True

MYSQL_HOST = 'localhost'
MYSQL_USER = 'tshutty'
MYSQL_PASSWD = 'PX77iADJ'
MYSQL_DB = 'tshutty'

SECRET_KEY = 'd41d8cd98f00b204e9800998ecf8427f'

LDAP_HOST =  'ldap-student.cs.unb.ca'

UPLOAD_FOLDER =  '/home1/ugrads/tshutty/repo/uploads'
#'/home/tye/codebase/AudioFileWebService/static/uploads' #'/home1/ugrads/tshutty/repo/uploads'

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'mp4', 'wma', 'm4a', 'ogg'}

SESSION = {"sid": "not a real session", "email": "err@unb.ca", "admin_status": 0}
