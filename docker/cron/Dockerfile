FROM ubuntu:latest

# Set environment variables
ENV TZ=Europe/Rome
ENV DEBIAN_FRONTEND=noninteractive          

# Install required packages
RUN apt update && apt upgrade -y && apt install python3 python3-pip cron git ansible -y

# Install dependencies
WORKDIR /usr/src/server_sniffer
RUN pip3 install --upgrade pip && \
    pip3 install "server_sniffer_utils @ git+https://github.com/GiuDaquan/server_sniffer_utils"

# Setup crontab
RUN (crontab -l 2>/dev/null; echo "*/1 * * * * /usr/bin/python3 /usr/src/server_sniffer/mongo_update.py >> /cron.log 2>&1") | crontab -