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

import subprocess

LOG = get_task_logger(__name__)


def progress_status_handler(output):
    if '%' in output:
        print('%s' % output)


def celery_log_handler(output):
    LOG.info(output)


def run(source_path, destination_path, output_handlers=()):
    cmd = ['rsync', '-ahHD', '--delete', '--no-inc-recursive', '--links',
           '--info=progress2', source_path, destination_path]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            output_list = output.split('\r')
            if len(output_list) > 0:
                output = output_list[-1].strip()
                for oh in output_handlers:
                    oh(output)
    return process.poll()
