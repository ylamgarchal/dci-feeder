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

import requests
import subprocess
import time


def test_sync():

    subprocess.check_output(["ssh", "root@rsyncd_sshd", "rm -rf", "-rf",
                             "/opt/compose/compose_cache"])
    ls = subprocess.check_output(["ssh", "root@rsyncd_sshd", "ls",
                                  "/opt/compose"])
    assert ls == ""

    sync = requests.post("http://127.0.0.1:5000/rhel/sync",
                         json={"topic": "rhel-8.2"})
    task_id = sync.json()["task_id"]
    current_status = sync.json()["event"]
    assert current_status == "SYNC_STARTED"
    while current_status == "SYNC_STARTED":
        status = requests.get("http://127.0.0.1:5000/rhel/status/%s" % task_id)
        current_status = status.json()["status"]
        time.sleep(1)

    diff = subprocess.check_output(["ssh", "root@rsyncd_sshd", "diff", "-r",
                                    "/opt/compose/compose_cache",
                                    "/opt/dci-feeder/tests/e2e/data/rhel/compose"])  # noqa
    assert diff == ""
