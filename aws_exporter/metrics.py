# -*- coding: utf-8 -*-
# ISC License
#
# Copyright 2019 FL Fintech E GmbH
#
# Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import logging
import time

from prometheus_client import Gauge
from prometheus_client.core import REGISTRY

from aws_exporter.aws.ec2 import AWSEC2MetricsCollector
from aws_exporter.aws.backup import AWSBackupMetricsCollector
from aws_exporter.aws.sns import AWSSNSMetricsCollector
from aws_exporter.aws.ses import AWSSESMetricsCollector

LOGGER = logging.getLogger(__name__)


class MetricsCollector:
    def __init__(self, metrics_config):
        if metrics_config['enable_ec2']:
            REGISTRY.register(AWSEC2MetricsCollector(config = metrics_config['ec2']))

        if metrics_config['enable_sns']:
            REGISTRY.register(AWSSNSMetricsCollector())

        if metrics_config['enable_backup']:
            REGISTRY.register(AWSBackupMetricsCollector())

        if metrics_config['enable_ses']:
            REGISTRY.register(AWSSESMetricsCollector())

    def run_loop(self, polling_interval_seconds = 30):
        while True:
            LOGGER.debug("sleeping for %s seconds", polling_interval_seconds)
            time.sleep(polling_interval_seconds)
