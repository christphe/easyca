FROM ubuntu:latest

RUN echo 'Acquire::http { Proxy "http://aptcacher.cloud.iscfrance.lan.bdx.sqli.com:3142"; };' > /etc/apt/apt.conf.d/02proxy
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y openssl python3
#RUN apt-get install -y software-properties-common
#RUN add-apt-repository -y ppa:certbot/certbot
#RUN apt-get update 
#RUN apt-get install -y certbot