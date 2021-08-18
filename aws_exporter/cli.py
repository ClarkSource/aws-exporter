# -*- coding: utf-8 -*-
# ISC License
#
# Copyright 2019 FL Fintech E GmbH
#
# Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import time
import logging

from prometheus_client import start_http_server

from aws_exporter.aws.backup import get_backup_jobs, get_backup_vaults
from aws_exporter.aws.sns import get_platform_applications
from aws_exporter.aws.ec2 import get_amis


def main():
    logging.basicConfig(level=logging.INFO)

    try:
        start_http_server(8000)

        while True:
            get_backup_vaults()
            get_backup_jobs()
            get_platform_applications()
            get_amis()

            time.sleep(10)
    except KeyboardInterrupt:
        exit(137)
