FROM python:3.11-rc-slim
RUN apt-get update
RUN apt-get -y install default-libmysqlclient-dev
RUN apt-get -y install gcc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /home/app/webapp 
# Install requirements
COPY ./ /home/app/webapp/
# RUN apt-get update
# RUN pip install --upgrade pip
RUN pip install -r /home/app/webapp/requirements.txt