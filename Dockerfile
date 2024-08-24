# Dockerfile to create image with cron services
FROM ubuntu:latest

ADD service.py /root/service.py
ADD config.ini /root/config.ini
ADD requirements.txt /root/requirements.txt

RUN chmod 0744 /root/service.py
RUN chmod 0644 /root/requirements.txt
RUN chmod 0644 /root/config.ini

RUN apt-get update
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN apt-get -y install python3-venv

# Create a virtual environment
RUN python3 -m venv /root/venv

# Install dependencies in the virtual environment
RUN /root/venv/bin/pip install -r /root/requirements.txt

# Use the virtual environment to run the script
CMD /root/venv/bin/python /root/service.py