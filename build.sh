#On server, run this script within ~/ChexyAgent folder containing ChexyAgent.py and wsgi.py
#do not copy ChexyAgentenv onto server, build it with this script on the server.

#chmod +x build.sh
#./build.sh

#based on https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04
sudo apt update
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
sudo apt install python3-venv
python3.6 -m venv Audioenv
source Audioenv/bin/activate
pip install wheel
pip install gunicorn flask flask-restful PyMySQL Flask-Session ldap3
# python3 -m pip install PyMySQL
#to test: 
#gunicorn --bind 0.0.0.0:5000 wsgi:app
deactivate
