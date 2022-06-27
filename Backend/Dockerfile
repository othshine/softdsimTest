FROM python:3.10.5-slim-bullseye
RUN apt-get update
RUN apt-get -y install default-libmysqlclient-dev
RUN apt-get -y install gcc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /home/app/webapp 
# Install requirements
# RUN apt-get update
# RUN pip install --upgrade pip
COPY ./Backend/requirements.txt /home/app/webapp/
RUN pip install -r /home/app/webapp/requirements.txt
