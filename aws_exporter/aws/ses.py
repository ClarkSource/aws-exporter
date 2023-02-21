# -*- coding: utf-8 -*-
# ISC License
#
# Copyright 2019 FL Fintech E GmbH
#
# Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import boto3
import logging

from prometheus_client.core import GaugeMetricFamily

from aws_exporter.aws import COMMON_LABELS
from aws_exporter.aws.sts import get_account_id
from aws_exporter.util import strget


SES = boto3.client("ses")
LOGGER = logging.getLogger(__name__)
SES_LABELS = COMMON_LABELS


class AWSSESMetricsCollector:
    def _metrics_containers(self):
        return {
            'aws_ses_send_quota_max': GaugeMetricFamily(
                'aws_ses_send_quota_max',
                'The maximum number of emails the user is allowed to send in a 24-hour interval.',
                labels=SES_LABELS
            ),
            'aws_ses_send_quota_rate_max': GaugeMetricFamily(
                'aws_ses_send_quota_rate_max',
                'The maximum number of emails that Amazon SES can accept from the user\'s account per second.',
                labels=SES_LABELS
            ),
            'aws_ses_send_quota_used': GaugeMetricFamily(
                'aws_ses_send_quota_used',
                'The number of emails sent during the previous 24 hours.',
                labels=SES_LABELS
            ),
        }

    def describe(self):
        return self._metrics_containers().values()

    def collect(self):
        metrics = self._metrics_containers()
        labels  = [get_account_id()]
        mapping = {
            'aws_ses_send_quota_max': 'Max24HourSend',
            'aws_ses_send_quota_rate_max': 'MaxSendRate',
            'aws_ses_send_quota_used': 'SentLast24Hours',
        }

        LOGGER.debug('querying sending quotas')

        response = SES.get_send_quota()

        for metric_key, response_key in mapping.items():
            metrics[metric_key].add_metric(labels, strget(response, response_key))
            yield metrics[metric_key]

        LOGGER.debug('finished querying sending quotas')

# -*- coding: utf-8 -*-
