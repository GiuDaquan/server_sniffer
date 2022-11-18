FROM ubuntu:latest

# Install required packages
RUN apt update && apt upgrade -y && apt install git python3 python3-pip -y

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create the server_sniffer user
RUN useradd -ms /bin/bash server_sniffer
USER server_sniffer
WORKDIR /home/server_sniffer

RUN ls
# Download and install server_sniffer
RUN git clone https://github.com/GiuDaquan/server_sniffer.git
WORKDIR /home/server_sniffer/server_sniffer/
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt