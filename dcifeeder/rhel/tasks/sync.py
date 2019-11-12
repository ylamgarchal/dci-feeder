# -*- coding: utf-8 -*-
#
# Copyright (C) Red Hat, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from celery.utils.log import get_task_logger
import requests
import time  # noqa


from dcifeeder.common import rsync
from dcifeeder import settings as s
from dcifeeder.celery_app import app

LOG = get_task_logger(__name__)


@app.task()
def sync(topic_name, task_id):
    LOG.info("sync topic %s" % topic_name)
    LOG.info("pull from rsyncd")
    handlers = (rsync.progress_status_handler, rsync.celery_log_handler)
    rsync.run('root@rsyncd_sshd::compose/', '/opt/compose_cache', handlers)
    rsync.run('/opt/compose_cache', 'root@rsyncd_sshd:/opt/compose', handlers)
    requests.post("%s/rhel/_events" % s.API_URL,
                  json={"event": "SYNC_SUCCESS",
                        "topic": topic_name,
                        "task_id": task_id})
