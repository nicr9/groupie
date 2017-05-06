FROM python:3
MAINTAINER Nic Roland "nicroland9@gmail.com"

WORKDIR /opt
COPY . /opt/
RUN pip install -r /opt/requirements.txt

ENTRYPOINT python3 /opt/groupie.py
