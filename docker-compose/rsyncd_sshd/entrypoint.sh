#!/bin/bash
set -e

exec /usr/sbin/sshd -E /var/log/sshd.log &

exec /usr/bin/rsync --daemon --no-detach --config /opt/dci-feeder/docker-compose/rsyncd_sshd/rsyncd.conf --log-file=/dev/stdout
