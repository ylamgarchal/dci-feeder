FROM centos:7

LABEL name="DCI Feeder API" version="0.0.1"
LABEL maintainer="DCI Team <distributed-ci@redhat.com>"

ENV LANG en_US.UTF-8

WORKDIR /opt/dci-feeder
COPY requirements.txt /opt/dci-feeder/

RUN yum -y install epel-release && \
    yum -y install python2-pip python2-setuptools \
    yum -y install python36 python36-devel python36-pip python36-setuptools && \
    yum -y install openssh-clients.x86_64 && \
    yum clean all && \
    pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -U tox && \
    pip install --no-cache-dir -r requirements.txt



RUN mkdir /root/.ssh
COPY docker-compose/ssh-keys/id_rsa /root/.ssh/
COPY docker-compose/ssh-keys/id_rsa.pub /root/.ssh/
RUN chmod 600 /root/.ssh/id_rsa

RUN sed -i 's/.*StrictHostKeyChecking.*/StrictHostKeyChecking no/g' /etc/ssh/ssh_config

ENV PYTHONPATH /opt/dci-feeder

EXPOSE 5000

ENTRYPOINT /opt/dci-feeder/bin/rundevserver
