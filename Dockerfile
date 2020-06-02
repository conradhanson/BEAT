FROM ubuntu:bionic

ENV PYTHONIOENCODING=utf8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/BusinessAggregator/"
ENV DISPLAY=:99

RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install \
    firefox \
    wget \
    curl \
    python3 python3-pip python3-setuptools \
    xvfb \
    vnc4server \
    dbus-x11

# install geckodriver
RUN GECKODRIVER_VERSION=`curl https://github.com/mozilla/geckodriver/releases/latest | grep -Po 'v[0-9]+.[0-9]+.[0-9]+'` && \
    wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz

COPY src/ BEAT/src/
WORKDIR /BEAT/src/
RUN pip3 install -r ./requirements.txt
RUN chmod a+x ./start.sh
ENTRYPOINT ["./start.sh"]