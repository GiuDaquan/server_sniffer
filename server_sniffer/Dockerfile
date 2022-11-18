FROM ubuntu:latest

# Install required packages
RUN apt update && apt upgrade -y
RUN apt install git -y

# Create the server_sniffer user
RUN useradd -ms /bin/bash server_sniffer
USER server_sniffer
WORKDIR /home/server_sniffer

# Setup GitHub SSH Authentication
RUN mkdir -m 0700 .ssh && ssh-keyscan github.com > .ssh/known_hosts

# Download and install server_sniffer_utils
RUN --mount=type=ssh,id=default git clone https://github.com/GiuDaquan/server_sniffer_utils.git
WORKDIR /home/server_sniffer/server_sniffer_utils




#
#COPY /home/giuseppe-daqanno
#
#
## set work directory
#WORKDIR /usr/src/server_sniffer
#
## set environment variables
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#
## install dependencies
#RUN pip install --upgrade pip
#COPY ./requirements.txt .
#RUN pip install -r requirements.txt
#
## copy project
#COPY . .