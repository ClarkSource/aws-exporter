# -*- coding: utf-8 -*-
# ISC License
#
# Copyright 2019 FL Fintech E GmbH
#
# Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import os
import time
import logging

from prometheus_client import start_http_server

from aws_exporter.aws.backup import get_backup_jobs, get_backup_vaults
from aws_exporter.aws.sns import get_platform_applications
from aws_exporter.aws.ec2 import get_amis, get_instances

LOGGER = logging.getLogger(__name__)


def main():
    delay = int(os.environ.get('AWS_EXPORTER_POLL_DELAY', 10))
    port = int(os.environ.get('AWS_EXPORTER_PORT', 8000))
    log_level = getattr(logging, os.environ.get('AWS_EXPORTER_LOG_LEVEL', 'info').upper())

    logging.basicConfig(level=log_level)
    logging.getLogger('botocore').setLevel(logging.WARN)
    logging.getLogger('urllib3').setLevel(logging.WARN)

    ami_owners = ['self']
    additional_ami_owners = os.environ.get('AWS_EXPORTER_EC2_AMI_OWNERS')

    if additional_ami_owners is not None:
        ami_owners.extend(additional_ami_owners.split(','))

    LOGGER.debug('getting amis from owners: %s', ami_owners)

    try:
        LOGGER.info('listening on port %d', port)

        start_http_server(port)

        while True:
            LOGGER.debug('querying resources')

            get_backup_vaults()
            get_backup_jobs()
            get_platform_applications()
            get_amis(ami_owners)
            get_instances()

            LOGGER.debug('sleeping %d seconds', delay)

            time.sleep(delay)
    except KeyboardInterrupt:
        exit(137)
