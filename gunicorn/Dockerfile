FROM python:3.10.4-slim-bullseye
RUN pip3 install gunicorn flask flask-wtf email_validator requests flask-login flask-sqlalchemy
COPY flask-project flask-project
CMD gunicorn --chdir flask-project app:app -w 2 --threads 2 -b unix:/shared/gunicorn.sock 
