sudo add-apt-repository ppa:certbot/certbot
sudo apt install python-certbot-nginx
sudo certbot --nginx -d ec2-18-218-32-161.us-east-2.compute.amazonaws.com
# Your cert will expire on 2021-05-12. To obtain a new or tweaked
#    version of this certificate in the future, simply run certbot again
#    with the "certonly" option.
#https://www.sslshopper.com/ssl-checker.html
