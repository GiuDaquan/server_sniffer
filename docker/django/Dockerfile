FROM ubuntu:latest

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install required packages
RUN apt update && apt upgrade -y && apt install git python3 python3-pip -y

# Create the server_sniffer user
RUN useradd -ms /bin/bash server_sniffer
USER server_sniffer
WORKDIR /home/server_sniffer

# Download and install server_sniffer
RUN echo ""
RUN git clone https://github.com/GiuDaquan/server_sniffer.git

# Install dependencies
WORKDIR /home/server_sniffer/server_sniffer/
ENV PATH="${PATH}:/home/server_sniffer/.local/bin"
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
