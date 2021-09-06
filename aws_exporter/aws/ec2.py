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

from aws_exporter.metrics import EC2_AMI_COLLECTOR_SUCCESS, EC2_AMI_CREATION_DATE, EC2_INSTANCE_COLLECTOR_SUCCESS, EC2_INSTANCE_CREATION_DATE
from aws_exporter.util import paginate, success_metric
from aws_exporter.aws.sts import get_account_id

EC2 = boto3.client("ec2")
LOGGER = logging.getLogger(__name__)


@success_metric(EC2_AMI_COLLECTOR_SUCCESS)
def get_amis(ami_owners):
    def observe(response):
        for image in response.get("Images", []):
            labels = [
                get_account_id(),
                image.get("ImageId"),
                image.get("Architecture"),
                image.get("EnaSupport"),
                image.get("Hypervisor"),
                image.get("Name"),
                image.get("OwnerId"),
                image.get("PlatformDetails"),
                image.get("Public"),
                image.get("RootDeviceName"),
                image.get("RootDeviceType"),
                image.get("VirtualizationType"),
            ]

            creation_date = time.strptime(image["CreationDate"], "%Y-%m-%dT%H:%M:%S.%fZ")

            EC2_AMI_CREATION_DATE.labels(*labels).set(time.mktime(creation_date))

    LOGGER.debug('querying EC2 AMIs')

    paginate(EC2.describe_images, observe, dict(Owners=ami_owners))

    LOGGER.debug('finished querying EC2 AMIs')


@success_metric(EC2_INSTANCE_COLLECTOR_SUCCESS)
def get_instances():
    def observe(response):
        for reservation in response.get("Reservations", []):
            for instance in reservation.get('Instances', []):
                metadata_options = instance['MetadataOptions']

                labels = [
                    get_account_id(),
                    instance.get('ImageId'),
                    instance.get('InstanceId'),
                    instance.get('State', {}).get('Name').lower(),
                    instance.get('InstanceType'),
                    instance.get('Architecture'),
                    instance.get('EbsOptimized'),
                    instance.get('EnaSupport'),
                    instance.get('Hypervisor'),
                    instance.get('RootDeviceName'),
                    instance.get('RootDeviceType'),
                    instance.get('SourceDestCheck'),
                    instance.get('VirtualizationType'),
                    metadata_options.get('HttpTokens'),
                    metadata_options.get('HttpPutResponseHopLimit'),
                    metadata_options.get('HttpEndpoint'),
                ]

                launch_time = instance['LaunchTime']

                EC2_INSTANCE_CREATION_DATE.labels(*labels).set(time.mktime(launch_time.timetuple()))

    LOGGER.debug('querying EC2 instances')

    paginate(EC2.describe_instances, observe)

    LOGGER.debug('finished querying EC2 instances')


# -*- coding: utf-8 -*-
