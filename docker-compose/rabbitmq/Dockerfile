FROM centos:7

LABEL name="RabbitMQ" version="0.0.1"
LABEL maintainer="DCI Team <distributed-ci@redhat.com>"

ENV LANG en_US.UTF-8

RUN yum -y install epel-release && \
    yum -y install rabbitmq-server.noarch

EXPOSE 5672

ENTRYPOINT rabbitmq-server
