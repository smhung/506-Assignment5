FROM python:3.10.4-slim-bullseye
RUN apt update
RUN apt install -y nginx
COPY 506-5-nginx-conf /etc/nginx/sites-available/default
#RUN ln -s /etc/nginx/sites-available/506-5 /etc/nginx/sites-enabled
#RUN service nginx restart
CMD ["nginx", "-g", "daemon off;"] 
#CMD gunicorn --chdir flask-project app:app -w 2 --threads 2 -b unix:/shared/gunicorn.sock 
