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

import logging
import os

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL',
                              'amqp://guest:guest@localhost:5672//')

CELERY_PROJECT_NAME = os.getenv('CELERY_PROJECT_NAME', 'dcifeeder')

API_URL = os.getenv('API_URL', 'http://127.0.0.1:5000')
API_DEBUG = os.getenv('API_DEBUG', False)

LOGLEVEL = logging.DEBUG
