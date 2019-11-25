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

import flask
import logging
import os
import signal
import sys

from dcifeeder.rhel import bp as rhel_bp
from dcifeeder import settings as s

LOG = logging.getLogger()


formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
streamhandler = logging.StreamHandler(stream=sys.stdout)
streamhandler.setFormatter(formatter)
LOG.addHandler(streamhandler)
LOG.setLevel(s.LOGLEVEL)


def create_app():
    app = flask.Flask(__name__)
    app.register_blueprint(rhel_bp)
    return app


def runserver(action='start'):
    pid_path = '/tmp/feeder.pid'

    def _start():
        if os.path.exists(pid_path):
            pid = open(pid_path, 'r').read()
            LOG.error('server already running, pid: %s' % pid)
            sys.exit(1)
        pid = os.getpid()
        with open(pid_path, 'w') as f:
            f.write(str(pid))
        LOG.debug('writing pid %s at %s' % (pid, pid_path))
        feederapp = create_app()
        feederapp.run(debug=s.API_DEBUG, threaded=True, host='0.0.0.0', use_reloader=False)  # noqa

    def _stop():
        if not os.path.exists(pid_path):
            return
        pid = open(pid_path, 'r').read()
        try:
            os.kill(int(pid), signal.SIGINT)
        except OSError as e:
            LOG.error('error while killing http server: %s' % str(e))
            sys.exit(1)
        os.remove(pid_path)
        LOG.debug('server stopped successfully')

    if action == 'start':
        _start()
    if action == 'stop':
        _stop()
    if action == 'restart':
        _stop()
        _start()
