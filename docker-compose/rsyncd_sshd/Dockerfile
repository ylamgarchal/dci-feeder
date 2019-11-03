FROM centos:7

LABEL name="DCI Feeder Rsync server and ssh server" version="0.0.1"
LABEL maintainer="DCI Team <distributed-ci@redhat.com>"

ENV LANG en_US.UTF-8


WORKDIR /opt/dci-feeder

RUN yum -y install rsync openssh-server.x86_64 && \
    yum clean all

RUN ssh-keygen -A

RUN mkdir /root/.ssh

ENTRYPOINT /opt/dci-feeder/docker-compose/rsyncd_sshd/entrypoint.sh
