FROM ubuntu:20.04

WORKDIR /cnp3

ENV DEBIAN_FRONTEND noninteractive 

RUN echo exit 0 > /usr/sbin/policy-rc.d && apt-get update && apt-get install apt-utils grub2 -y 


ADD exercises/ /cnp3

# google-mock libgmock-dev  libboost-dev

RUN apt-get install binutils git sudo   python3-pip  -y && \
    pip3 install --upgrade git+https://github.com/akemery/ipmininet.git@v0.9 && \ 
    apt-get -y install debconf-utils && echo resolvconf resolvconf/linkify-resolvconf boolean false | debconf-set-selections && \
    echo exit 0 > /usr/sbin/policy-rc.d && \
    python3 -m ipmininet.install -a
    
CMD [ "echo", "welcome to ipmininet" ]
