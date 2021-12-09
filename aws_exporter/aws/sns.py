# -*- coding: utf-8 -*-
# ISC License
#
# Copyright 2019 FL Fintech E GmbH
#
# Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import boto3
import datetime
import logging

from prometheus_client.core import GaugeMetricFamily
from aws_exporter.aws import COMMON_LABELS
from aws_exporter.util import paginate
from aws_exporter.aws.sts import get_account_id

SNS = boto3.client('sns')
LOGGER = logging.getLogger(__name__)
SNS_PLATFORM_APPLICATION_LABELS = COMMON_LABELS + [
    'sns_platform_application_name',
]


class AWSSNSMetricsCollector:
    def __init__(self, config = None):
        self.ami_owners = config.get('ami_owners', {}) if config is not None else ['self']

    def describe(self):
        yield GaugeMetricFamily('sns_platform_application_enabled', 'AWS SNS platform application enabled', labels=SNS_PLATFORM_APPLICATION_LABELS)
        yield GaugeMetricFamily('sns_platform_application_cert_expiry', 'AWS SNS platform application certificate expiration date', labels=SNS_PLATFORM_APPLICATION_LABELS)

    def collect(self):
        yield from self.fetch_platform_applications()

    def fetch_platform_applications(self):
        """
        {
            'PlatformApplications': [
                {
                    'PlatformApplicationArn': 'arn:aws:sns:xx-xxxxx-x:XXXXXXXXXXXX:app/APNS/yyyyyyy',
                    'Attributes': {
                        'SuccessFeedbackSampleRate': '100',
                        'Enabled': 'true',
                        'AppleCertificateExpirationDate': '2020-04-09T14:27:56Z'
                    }
                },
                {
                    'PlatformApplicationArn': 'arn:aws:sns:xx-xxxxx-x:XXXXXXXXXXXX:app/APNS_SANDBOX/yyyyyy',
                    'Attributes': {
                        'SuccessFeedbackSampleRate': '100',
                        'Enabled': 'true',
                        'AppleCertificateExpirationDate': '2020-03-10T14:25:40Z'
                    }
                },
                {
                    'PlatformApplicationArn': 'arn:aws:sns:xx-xxxxx-x:XXXXXXXXXXXX:app/GCM/yyyyyyy',
                    'Attributes': {
                        'Enabled': 'true'
                    }
                }
            ],
            'ResponseMetadata': {
                'RequestId': '2k3j3215-5539-2315-k123-3kjh152kjh67',
                'HTTPStatusCode': 200,
                'HTTPHeaders': {
                    'x-amzn-requestid': 'ksajhdas-7sa1-kj22-ka2a-ksajd2eo2i19',
                    'content-type': 'text/xml',
                    'content-length': '1736',
                    'date': 'Wed, 11 Mar 2020 09:10:54 GMT'
                },
                'RetryAttempts': 0
            }
        }
        """
        sns_platform_application_enabled = GaugeMetricFamily('sns_platform_application_enabled', 'AWS SNS platform application enabled', labels=SNS_PLATFORM_APPLICATION_LABELS)
        sns_platform_application_cert_expiry = GaugeMetricFamily('sns_platform_application_cert_expiry', 'AWS SNS platform application certificate expiration date', labels=SNS_PLATFORM_APPLICATION_LABELS)

        def observe(response):
            for application in response.get('PlatformApplications', []):
                name = application['PlatformApplicationArn'].split(':')[-1]
                attributes = application['Attributes']

                labels = [
                    get_account_id(),
                    name,
                ]

                sns_platform_application_enabled.add_metric(labels,
                    1 if attributes['Enabled'] == 'true' else 0)

                if 'AppleCertificateExpirationDate' in attributes:
                    expiry = datetime.datetime.strptime(attributes['AppleCertificateExpirationDate'], '%Y-%m-%dT%H:%M:%SZ')

                    sns_platform_application_cert_expiry.add_metric(labels, expiry.timestamp())

        LOGGER.debug('querying SNS platform applications')

        paginate(SNS.list_platform_applications, observe)

        yield sns_platform_application_enabled
        yield sns_platform_application_cert_expiry

        LOGGER.debug('finished querying SNS platform applications')

# -*- coding: utf-8 -*-
