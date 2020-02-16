FROM python:3.7
#ENV TZ=Europe/Moscow

RUN mkdir /app
WORKDIR /app

RUN apt-get update
#RUN apt-get install -y python3.6 python3-pip
RUN apt-get -y install postgresql

COPY . /app/
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# EXPOSE 8000

# RUN psql -h 'localhost' -d postgres -f init.sql

