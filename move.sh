
mkdir ../Audio
cp Audio.service build.sh *.py ../Audio
cp -r db static ../Audio
scp -i ../ChexyAIHost_key.pem -r ../Audio azureuser@52.138.40.34:~
rm -rf ../Audio
ssh -o ServerAliveInterval=100000000 -i ../ChexyAIHost_key.pem azureuser@52.138.40.34

# then on server: cd Audio
# chmod +x build.sh deploy.sh http_certification.sh app.py
# ./build.sh
# ./deploy.sh
# ./http_certification.sh
