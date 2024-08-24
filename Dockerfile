# Dockerfile to create image with cron services
FROM ubuntu:latest

ADD service.py /root/service.py
ADD requirements.txt /root/requirements.txt

RUN chmod 0744 /root/service.py
RUN chmod 0644 /root/requirements.txt

RUN apt-get update
RUN apt-get -y install python3
RUN apt-get -y install python3-pip

RUN pip install -r /root/requirements.txt

RUN touch /var/log/cron.log

CMD python3 /root/service.py
