# -*- coding: utf-8 -*-
# ISC License
#
# Copyright 2019 FL Fintech E GmbH
#
# Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import os
import boto3
import time
import logging

from aws_exporter.metrics import (EC2_AMI_COLLECTOR_SUCCESS, EC2_AMI_CREATION_DATE)
from aws_exporter.util import paginate, success_metric
from aws_exporter.aws.sts import get_account_id

EC2 = boto3.client('ec2')
LOGGER = logging.getLogger(__name__)


@success_metric(EC2_AMI_COLLECTOR_SUCCESS)
def get_amis(ami_owners):
    def observe(response):
        for image in response.get('Images', []):
            labels = [
                get_account_id(),
                image['Architecture'],
                image['EnaSupport'],
                image['Hypervisor'],
                image['ImageId'],
                image['Name'],
                image['OwnerId'],
                image['PlatformDetails'],
                image['Public'],
                image['RootDeviceName'],
                image['RootDeviceType'],
                image['VirtualizationType'],
            ]

            creation_date = time.strptime(image['CreationDate'], '%Y-%m-%dT%H:%M:%S.%fZ')

            EC2_AMI_CREATION_DATE.labels(*labels).set(time.mktime(creation_date))

    paginate(EC2.describe_images, observe, dict(Owners=ami_owners))

# -*- coding: utf-8 -*-
