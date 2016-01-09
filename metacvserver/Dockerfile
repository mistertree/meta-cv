FROM ubuntu:14.04

RUN apt-get -y update; apt-get -y install apt-transport-https curl python3.4 \
build-essential python3-pip libpq-dev libtiff4-dev libjpeg8-dev zlib1g-dev \
libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev

RUN sh -c 'curl https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -'
RUN sh -c 'curl https://storage.googleapis.com/download.dartlang.org/linux/debian/dart_stable.list > /etc/apt/sources.list.d/dart_stable.list'
RUN apt-get -y update; apt-get -y install dart

RUN pip3 install uwsgi pylint

RUN pip3 install django==1.9 psycopg2==2.6 pillow==3.0.0 \
django-sass-processor==0.3.3 libsass==0.10.0

#Waiting for the official release of the new version of this library.
RUN apt-get -y install git
RUN git clone https://github.com/jcassee/django-analytical /tmp/repo; git -C \
/tmp/repo/ checkout 735d86d16fc048c048b20b622b5f655fb2a28e90
RUN cd /tmp/repo/; python3.4 setup.py install
RUN rm -r /tmp/repo/
RUN apt-get -y remove git; apt-get -y autoremove

WORKDIR /var/django/metacvserver/

ADD common common

ADD cv/static/cv/*.dart ./cv/static/cv/
RUN mkdir -p /var/django/metacvserver_compiledjs/cv/
RUN /usr/lib/dart/bin/dart2js --no-source-maps -m --fatal-warnings -pcommon/ --out=/var/django/metacvserver_compiledjs/cv/cv_bootstrap.js cv/static/cv/cv_bootstrap.dart
RUN rm cv/static/cv/*.dart

ADD video/static/video/*.dart ./video/static/video/
RUN mkdir -p /var/django/metacvserver_compiledjs/video/
RUN /usr/lib/dart/bin/dart2js --no-source-maps -m --fatal-warnings -pcommon/ --out=/var/django/metacvserver_compiledjs/video/video_bootstrap.js video/static/video/video_bootstrap.dart
RUN rm video/static/video/*.dart

RUN rm common/metacvserver_common/*.dart

RUN mkdir -p /var/django/metacvserver_compiledcss/

ADD . /var/django/metacvserver/
