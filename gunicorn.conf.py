PYTHONUNBUFFERED = True 
#works, but causes crash, e.g.:
# [2021-05-06 19:33:13 +0000] [32701] [INFO] Starting gunicorn 20.1.0
# [2021-05-06 19:33:13 +0000] [32701] [DEBUG] Arbiter booted
# [2021-05-06 19:33:13 +0000] [32701] [INFO] Listening at: unix:Audio.sock (32701)
# [2021-05-06 19:33:13 +0000] [32701] [INFO] Using worker: sync
# [2021-05-06 19:33:13 +0000] [318] [INFO] Booting worker with pid: 318
# [2021-05-06 19:33:13 +0000] [325] [INFO] Booting worker with pid: 325
# [2021-05-06 19:33:13 +0000] [326] [INFO] Booting worker with pid: 326
# [2021-05-06 19:33:13 +0000] [32701] [DEBUG] 3 workers
# [2021-05-06 19:33:35 +0000] [318] [DEBUG] GET /audio
# [2021-05-06 19:33:35 +0000] [325] [DEBUG] GET /audio/static/app.js
# [2021-05-06 19:33:35 +0000] [326] [DEBUG] GET /audio/static/schools.css
# [2021-05-06 19:37:37 +0000] [32701] [INFO] Handling signal: term
# [2021-05-06 19:37:37 +0000] [318] [INFO] Worker exiting (pid: 318)
# hello
# [2021-05-06 19:37:37 +0000] [325] [INFO] Worker exiting (pid: 325)
# [2021-05-06 19:37:37 +0000] [326] [INFO] Worker exiting (pid: 326)
# [2021-05-06 19:37:37 +0000] [32701] [WARNING] Worker with pid 325 was terminated due to signal 15
# [2021-05-06 19:37:37 +0000] [32701] [WARNING] Worker with pid 326 was terminated due to signal 15
# [2021-05-06 19:37:37 +0000] [32701] [INFO] Shutting down: Master
