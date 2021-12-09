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

from prometheus_client.core import GaugeMetricFamily

from aws_exporter.aws import COMMON_LABELS
from aws_exporter.aws.sts import get_account_id
from aws_exporter.util import paginate, strget


EC2 = boto3.client("ec2")
LOGGER = logging.getLogger(__name__)
EC2_AMI_LABELS = COMMON_LABELS + [
    'ec2_ami',
    'ec2_architecture',
    'ec2_ena_support',
    'ec2_hypervisor',
    'ec2_image_name',
    'ec2_owner_id',
    'ec2_platform',
    'ec2_public',
    'ec2_root_device_name',
    'ec2_root_device_type',
    'ec2_virtualization_type',
]
EC2_INSTANCE_LABELS = COMMON_LABELS + [
    'ec2_ami',
    'ec2_instance_id',
    'ec2_instance_state',
    'ec2_instance_type',
    'ec2_architecture',
    'ec2_ebs_optimized',
    'ec2_ena_support',
    'ec2_hypervisor',
    'ec2_root_device_name',
    'ec2_root_device_type',
    'ec2_source_dest_check',
    'ec2_virtualization_type',
    'ec2_metadata_options_http_tokens',
    'ec2_metadata_options_http_put_response_hop_limit',
    'ec2_metadata_options_endpoint',
]


class AWSEC2MetricsCollector:
    def __init__(self, config = None):
        self.ami_owners = config.get('ami_owners', {}) if config is not None else ['self']

    def describe(self):
        yield GaugeMetricFamily('ec2_ami_creation_date', 'AWS EC2 AMI creation date in unix epoch', labels=EC2_AMI_LABELS)
        yield GaugeMetricFamily('ec2_instance_creation_date', 'AWS EC2 instance creation date in unix epoch', labels=EC2_INSTANCE_LABELS)

    def collect(self):
        yield from self.fetch_amis()
        yield from self.fetch_instances()

    def fetch_amis(self):
        ec2_ami_creation_date = GaugeMetricFamily('ec2_ami_creation_date', 'AWS EC2 AMI creation date in unix epoch', labels=EC2_AMI_LABELS)

        def observe(response):
            for image in response.get("Images", []):
                labels = [
                    get_account_id(),
                    strget(image, "ImageId"),
                    strget(image, "Architecture"),
                    strget(image, "EnaSupport"),
                    strget(image, "Hypervisor"),
                    strget(image, "Name"),
                    strget(image, "OwnerId"),
                    strget(image, "PlatformDetails"),
                    strget(image, "Public"),
                    strget(image, "RootDeviceName"),
                    strget(image, "RootDeviceType"),
                    strget(image, "VirtualizationType"),
                ]

                creation_date = time.strptime(image["CreationDate"], "%Y-%m-%dT%H:%M:%S.%fZ")

                ec2_ami_creation_date.add_metric(labels, time.mktime(creation_date))

        LOGGER.debug('querying EC2 AMIs')

        paginate(EC2.describe_images, observe, dict(Owners=self.ami_owners))

        yield ec2_ami_creation_date

        LOGGER.debug('finished querying EC2 AMIs')

    def fetch_instances(self):
        ec2_instance_creation_date = GaugeMetricFamily('ec2_instance_creation_date', 'AWS EC2 instance creation date in unix epoch', labels=EC2_INSTANCE_LABELS)

        def observe(response):
            for reservation in response.get("Reservations", []):
                for instance in reservation.get('Instances', []):
                    metadata_options = instance['MetadataOptions']

                    labels = [
                        get_account_id(),
                        strget(instance, 'ImageId'),
                        strget(instance, 'InstanceId'),
                        strget(instance.get('State', {}), 'Name', '').lower(),
                        strget(instance, 'InstanceType'),
                        strget(instance, 'Architecture'),
                        strget(instance, 'EbsOptimized'),
                        strget(instance, 'EnaSupport'),
                        strget(instance, 'Hypervisor'),
                        strget(instance, 'RootDeviceName'),
                        strget(instance, 'RootDeviceType'),
                        strget(instance, 'SourceDestCheck'),
                        strget(instance, 'VirtualizationType'),
                        strget(metadata_options, 'HttpTokens'),
                        strget(metadata_options, 'HttpPutResponseHopLimit'),
                        strget(metadata_options, 'HttpEndpoint'),
                    ]

                    launch_time = instance['LaunchTime']

                    ec2_instance_creation_date.add_metric(labels, time.mktime(launch_time.timetuple()))

        LOGGER.debug('querying EC2 instances')

        paginate(EC2.describe_instances, observe)

        yield ec2_instance_creation_date

        LOGGER.debug('finished querying EC2 instances')

# -*- coding: utf-8 -*-
