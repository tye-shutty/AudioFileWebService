
mkdir ../Audio

cp Audio.service build.sh app.py authorize.py file.py files.py folder.py folders.py gunicorn.conf.py \
helpers.py signin.py user.py users.py *.log ../Audio

mkdir ../Audio/static
mkdir ../Audio/static/uploads
mkdir ../Audio/static/openapi
cp static/app.js static/index.html static/schools.css ../Audio/static
cp static/openapi/index.html ../Audio/static/openapi

cp -r db ../Audio

scp -i ../ChexyAIHost_key.pem -r ../Audio azureuser@52.138.36.161:~
rm -rf ../Audio
ssh -o ServerAliveInterval=100000000 -i ../ChexyAIHost_key.pem azureuser@52.138.36.161

# then on server: cd Audio
# chmod +x build.sh deploy.sh http_certification.sh app.py
# ./build.sh
# ./deploy.sh
# ./http_certification.sh
