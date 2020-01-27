FROM ubuntu:18.10
MAINTAINER stevesl@umich.edu

# Copying over the requirements.txt
COPY . /server

# Installing packages needed for installing python, pip, and vim.
RUN apt-get update
RUN apt -y install python3-pip
RUN apt -y install vim
RUN apt -y install curl
RUN apt -y install net-tools

# Installing python packages from requirements.txt
# into the "packages" directory.
#RUN pip3 install -r requirements.txt -t ./packages

# Installing requirements.txt packages.
RUN pip3 install -r /server/requirements.txt

CMD python3 server/demo.py
