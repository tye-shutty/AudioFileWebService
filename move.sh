
mkdir ../Audio
cp Audio Audio.service deploy.sh build.sh *.py https_certification.sh ../Audio
cp -r db ../Audio
cp -r static ../Audio
cp -r uploads ../Audio
scp -i ~/.ssh/aws_HP.pem -r ../Audio ubuntu@ec2-18-218-32-161.us-east-2.compute.amazonaws.com:~
rm -rf ../Audio
ssh -i ~/.ssh/aws_HP.pem ubuntu@ec2-18-218-32-161.us-east-2.compute.amazonaws.com

# then on server: cd Audio
# chmod +x build.sh deploy.sh http_certification.sh app.py
# ./build.sh
# ./deploy.sh
# ./http_certification.sh
