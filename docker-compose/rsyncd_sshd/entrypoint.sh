#!/bin/bash
set -e

chmod 400 /root/.ssh/authorized_keys
chown root:root /root/.ssh/authorized_keys

exec /usr/sbin/sshd &

exec /usr/bin/rsync --daemon --no-detach --config /opt/dci-feeder/docker-compose/rsyncd_sshd/rsyncd.conf --log-file=/dev/stdout
