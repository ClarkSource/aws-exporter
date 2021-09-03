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

from aws_exporter.metrics import (
    SNS_PLATFORM_APPLICATION_COLLECTOR_SUCCESS,
    SNS_PLATFORM_APPLICATION_CERT_EXPIRY,
    SNS_PLATFORM_APPLICATION_ENABLED)

from aws_exporter.util import paginate, success_metric
from aws_exporter.aws.sts import get_account_id

SNS = boto3.client('sns')
LOGGER = logging.getLogger(__name__)


@success_metric(SNS_PLATFORM_APPLICATION_COLLECTOR_SUCCESS)
def get_platform_applications():
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

    def observe(response):
        for application in response.get('PlatformApplications', []):
            name = application['PlatformApplicationArn'].split(':')[-1]
            attributes = application['Attributes']

            labels = [
                get_account_id(),
                name,
            ]

            SNS_PLATFORM_APPLICATION_ENABLED.labels(*labels).set(
                1 if attributes['Enabled'] == 'true' else 0)

            if 'AppleCertificateExpirationDate' in attributes:
                expiry = datetime.datetime.strptime(attributes['AppleCertificateExpirationDate'], '%Y-%m-%dT%H:%M:%SZ')

                SNS_PLATFORM_APPLICATION_CERT_EXPIRY.labels(*labels).set(expiry.timestamp())

    LOGGER.debug('querying SNS platform applications')

    paginate(SNS.list_platform_applications, observe)

    LOGGER.debug('finished querying SNS platform applications')

