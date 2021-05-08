# AudioFileWebService

cs3103 project. Upload files, download files, play them.
This site currently works on Firefox with mp3 and ogg files of less than 2 MB in size.
You can play multiple files at the same time! You can organize your 
files into folders. The volume bar is exponential because I have often fiddled with 
volume controls in the past where the volume was way too loud and I had difficultly making the volume 1% not 2%.

The search function uses SQL rules, e.g. % is a wildcard. If this site is running on the UNB computer, it may not be
able to serve many files, it may serve them slowly, and it may cause the server to freeze. 
Just test with files of 1-2 MB.

There is an account called "admin" that you can demo. The password is anything longer than an empty string.
This site is designed to be run on Firefox, Chrome and other browsers may behave unexpectedly.

This site was designed for cs3103, UNB in 2021 by Tye Shutty. Audīsne mē? is Latin for "Are you listening to me?"

Please don't worry about us storing some passwords on github, this site is not being hosted on the public internet.

View errors on server: 
systemctl status Audio
journalctl -u Audio.service
<!-- https://mattsegal.dev/django-gunicorn-nginx-logging.html -->
vim /home/azureuser/Audio/audio_error.log
vim /home/azureuser/Audio/access.log
tail -n 5
or less, shift-g to go to end

Git help:
git filter-branch --tree-filter 'rm -f settings.py' -- --all
git push origin media:tyeshutty

increase server request size:
https://serverfault.com/questions/814767/413-request-entity-too-large-in-nginx-with-client-max-body-size-set
sudo vim /etc/nginx/nginx.conf
client_max_body_size 10M; (in http section)
sudo service nginx restart

these settings may be helpful in the future:
https://stackoverflow.com/questions/38873780/nginx-returns-internal-server-error-when-uploading-large-files-several-gb
    client_body_timeout 300s;

    client_body_in_file_only clean;
    client_body_buffer_size 16K;
    client_body_temp_path /home/nginx/client_body_temp;
