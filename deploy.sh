#Only run on server, requires nginx, the build.sh script must be run first, and
#Audio.service and Audio files must be in the ~/Audio folder
#dist folder must be in home directory e.g. ~/dist/index.html
#those files require the user name to be engg4000

cd ~/Audio
sudo apt install nginx
sudo cp Audio.service /etc/systemd/system/Audio.service
sudo systemctl start Audio
sudo systemctl restart Audio
sudo systemctl enable Audio
sudo cp Audio /etc/nginx/sites-available/Audio
sudo mv /etc/nginx/sites-enabled/Audio ~/Audio/oldAudio
sudo ln -s /etc/nginx/sites-available/Audio /etc/nginx/sites-enabled
sudo rm /etc/nginx/sites-enabled/default
sudo systemctl daemon-reload
sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'
sudo ufw allow 80
sudo ufw allow 443
