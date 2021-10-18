#!/bin/sh

# run db migrations on startup
/usr/local/bin/flask db upgrade

# gunicorn is necessary to support graceful shutdown on TERM signal https://docs.gunicorn.org/en/stable/signals.html
# use exec to run as pid 1
exec gunicorn --chdir /app app:app -w 2 --threads 2 -b 0.0.0.0:8080
