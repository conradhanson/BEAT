FROM ubuntu:bionic

# SET ENV VARS
ENV PYTHONIOENCODING=utf8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DISPLAY=:99

# INSTALL DEPENDENCIES
RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install \
    curl \
    dbus-x11 \
    firefox \
    python3 python3-pip python3-setuptools \
    vnc4server \
    wget \
    xvfb

# INSTALL GeckoDriver
RUN GECKODRIVER_VERSION=`curl https://github.com/mozilla/geckodriver/releases/latest | grep -Po 'v[0-9]+.[0-9]+.[0-9]+'` && \
    wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz

# MOVE PROJECT FILES TO IMAGE
COPY src/ BEAT/src/
WORKDIR /BEAT/src/

# INSTALL PYTHON DEPENDENCIES
RUN pip3 install -r ./requirements.txt

# SET CONTAINER ENTRY SCRIPT
RUN chmod a+x ./start.sh
ENTRYPOINT ["./start.sh"]