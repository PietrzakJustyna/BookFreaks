FROM ubuntu:latest
RUN apt-get update
FROM python:3
WORKDIR /usr/src/app
CMD python
RUN pip install django
RUN pip install psycopg2-binary
RUN pip install django-crispy-forms
COPY . /app
