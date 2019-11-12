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

from dcifeeder.common.tasks import notifications
from dcifeeder.rhel import bp
from dcifeeder.rhel.tasks import sync as rhel_sync

import flask
import logging
import uuid

LOG = logging.getLogger(__name__)


@bp.route("/sync", methods=["POST"])
def sync():
    topic = flask.request.json.get("topic")
    task_id = str(uuid.uuid4())
    rhel_sync.sync.delay(topic, task_id)
    with open("/opt/%s" % task_id, "w") as f:
        f.write("SYNC_STARTED")
        return flask.jsonify(
            {"event": "SYNC_STARTED",
             "topic": topic,
             "task_id": task_id}), 201


@bp.route("/status/<task_id>", methods=["GET"])
def get_task_status(task_id):
    with open("/opt/%s" % task_id, "r") as f:
        status = f.read()
        return flask.jsonify(
            {"task_id": task_id,
             "status": status}), 200


@bp.route("/_events", methods=["POST"])
def handle_events():
    payload = flask.request.json
    event = payload["event"]
    if event == "SYNC_SUCCESS":
        task_id = payload['task_id']
        LOG.info("rhel topic %s sync succeed, task_id=%s" % (payload["topic"],
                                                             task_id))
        LOG.info("send notifications by mails")
        with open("/opt/%s" % task_id, "w") as f:
            f.write(event)
        notifications.send_mails.delay({})

    return flask.jsonify(
        {"type": "ACK"}), 200
