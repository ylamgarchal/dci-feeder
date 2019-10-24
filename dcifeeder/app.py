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

import celery
import flask
import logging
import sys

from dcifeeder.rhel import bp as rhel_bp
from dcifeeder import settings as s

LOG = logging.getLogger()


def configure_root_logger(loglevel):
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    streamhandler = logging.StreamHandler(stream=sys.stdout)
    streamhandler.setFormatter(formatter)
    LOG.addHandler(streamhandler)
    LOG.setLevel(loglevel)


def create_app():
    configure_root_logger(s.LOGLEVEL)
    app = flask.Flask(__name__)
    app.register_blueprint(rhel_bp)

    return app
