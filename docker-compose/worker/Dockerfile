FROM centos:7

LABEL name="DCI Feeder Worker" version="0.0.1"
LABEL maintainer="DCI Team <distributed-ci@redhat.com>"

ENV LANG en_US.UTF-8


WORKDIR /opt/dci-feeder
COPY requirements.txt /opt/dci-feeder/

RUN yum -y install epel-release && \
    yum -y install python2-pip python2-setuptools \
    yum -y install python34 python34-devel python34-pip python34-setuptools && \
    yum clean all && \
    pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -U tox && \
    pip install --no-cache-dir -r requirements.txt


ENTRYPOINT celery -A dcifeeder.celery_app:app worker --loglevel=info
