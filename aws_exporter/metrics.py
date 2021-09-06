# -*- coding: utf-8 -*-
# ISC License
#
# Copyright 2019 FL Fintech E GmbH
#
# Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from prometheus_client import Gauge

COMMON_LABELS = ['aws_account_id'] # aws_account_id

###############################################################################
# AWS Backup

BACKUP_JOB_LABELS = COMMON_LABELS + [
    'creation_date',
    'completion_date',
    'backup_job_id',
    'backup_job_state',
    'backup_rule_id',
    'backup_plan_id',
    'backup_vault_name',
]

BACKUP_JOB_COLLECTOR_SUCCESS = Gauge(
    'aws_backup_job_collector_success', 'AWS Backup job collector success', COMMON_LABELS)

BACKUP_JOB_SIZE_BYTES = Gauge(
    'aws_backup_job_size_bytes', 'AWS Backup job size in bytes', BACKUP_JOB_LABELS)
BACKUP_JOB_PERCENT_DONE = Gauge(
    'aws_backup_job_percent_done', 'AWS Backup job percent done', BACKUP_JOB_LABELS)

BACKUP_VAULT_LABELS = COMMON_LABELS + ['backup_vault_name']

BACKUP_VAULT_COLLECTOR_SUCCESS = Gauge(
    'aws_backup_vault_collector_success', 'AWS Backup vault collector success', COMMON_LABELS)

BACKUP_VAULT_RECOVERY_POINTS = Gauge(
    'aws_backup_vault_recovery_points', 'AWS Backup vault number of recovery points', BACKUP_VAULT_LABELS)

###############################################################################
# AWS SNS push notifications

SNS_PLATFORM_APPLICATION_LABELS = COMMON_LABELS + [
    'sns_platform_application_name',
]

SNS_PLATFORM_APPLICATION_COLLECTOR_SUCCESS = Gauge(
    'sns_platform_application_collector_success', 'AWS SNS platform application collector success', COMMON_LABELS)

SNS_PLATFORM_APPLICATION_ENABLED = Gauge(
    'sns_platform_application_enabled', 'AWS SNS platform application enabled', SNS_PLATFORM_APPLICATION_LABELS)

SNS_PLATFORM_APPLICATION_CERT_EXPIRY = Gauge(
    'sns_platform_application_cert_expiry', 'AWS SNS platform application certificate expiration date', SNS_PLATFORM_APPLICATION_LABELS)


###############################################################################
# AWS EC2 AMIs

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

EC2_AMI_COLLECTOR_SUCCESS = Gauge(
    'ec2_ami_collector_success', 'AWS EC2 AMI collector success', COMMON_LABELS)

EC2_AMI_CREATION_DATE = Gauge(
    'ec2_ami_creation_date', 'AWS EC2 AMI creation date in unix epoch', EC2_AMI_LABELS)

###############################################################################
# AWS EC2 Instances

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

EC2_INSTANCE_COLLECTOR_SUCCESS = Gauge(
    'ec2_instance_collector_success', 'AWS EC2 instance collector success', COMMON_LABELS)

EC2_INSTANCE_CREATION_DATE = Gauge(
    'ec2_instance_creation_date', 'AWS EC2 instance creation date in unix epoch', EC2_INSTANCE_LABELS)
