# -*- coding: utf-8 -*-
# ISC License
#
# Copyright 2019 FL Fintech E GmbH
#
# Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import datetime
import logging

import boto3
from prometheus_client.core import GaugeMetricFamily
from aws_exporter.aws import COMMON_LABELS
from aws_exporter.aws.sts import get_account_id
from aws_exporter.util import paginate, strget

BACKUP = boto3.client("backup")
LOGGER = logging.getLogger(__name__)
BACKUP_JOB_LABELS = COMMON_LABELS + [
    'creation_date',
    'completion_date',
    'backup_job_id',
    'backup_job_state',
    'backup_rule_id',
    'backup_plan_id',
    'backup_vault_name',
]
BACKUP_VAULT_LABELS = COMMON_LABELS + [
    'backup_vault_name'
]


class AWSBackupMetricsCollector:
    def __init__(self, config = None):
        self.ami_owners = config.get('ami_owners', {}) if config is not None else ['self']

    def describe(self):
        yield GaugeMetricFamily('aws_backup_job_size_bytes', 'AWS Backup job size in bytes', labels=BACKUP_JOB_LABELS)
        yield GaugeMetricFamily('aws_backup_job_percent_done', 'AWS Backup job percent done', labels=BACKUP_JOB_LABELS)
        yield GaugeMetricFamily('aws_backup_vault_recovery_points', 'AWS Backup vault number of recovery points', labels=BACKUP_VAULT_LABELS)

    def collect(self):
        yield from self.get_backup_jobs()
        yield from self.get_backup_vaults()

    def get_backup_jobs(self):
        """
        {
            'BackupJobs': [
                {
                    'BackupJobId': 'string',
                    'BackupVaultName': 'string',
                    'BackupVaultArn': 'string',
                    'RecoveryPointArn': 'string',
                    'ResourceArn': 'string',
                    'CreationDate': datetime(2015, 1, 1),
                    'CompletionDate': datetime(2015, 1, 1),
                    'State': 'CREATED'|'PENDING'|'RUNNING'|'ABORTING'|'ABORTED'|'COMPLETED'|'FAILED'|'EXPIRED',
                    'StatusMessage': 'string',
                    'PercentDone': 'string',
                    'BackupSizeInBytes': 123,
                    'IamRoleArn': 'string',
                    'CreatedBy': {
                        'BackupPlanId': 'string',
                        'BackupPlanArn': 'string',
                        'BackupPlanVersion': 'string',
                        'BackupRuleId': 'string'
                    },
                    'ExpectedCompletionDate': datetime(2015, 1, 1),
                    'StartBy': datetime(2015, 1, 1),
                    'ResourceType': 'string',
                    'BytesTransferred': 123
                },
            ],
            'NextToken': 'string'
        }
        """
        backup_job_size_bytes = GaugeMetricFamily('aws_backup_job_size_bytes', 'AWS Backup job size in bytes', labels=BACKUP_JOB_LABELS)
        backup_job_percent_done = GaugeMetricFamily('aws_backup_job_percent_done', 'AWS Backup job percent done', labels=BACKUP_JOB_LABELS)

        def observe(response):
            for job in response.get("BackupJobs", []):
                labels = [
                    get_account_id(),
                    strget(job, 'CreationDate'),
                    strget(job, 'CompletionDate'),
                    strget(job, 'BackupJobId'),
                    strget(job, 'State'),
                    strget(job['CreatedBy'], 'BackupRuleId'),
                    strget(job['CreatedBy'], 'BackupPlanId'),
                    strget(job, 'BackupVaultName'),
                ]

                backup_job_percent_done.add_metric(labels, float(job["PercentDone"]))

                if "BackupSizeInBytes" in job:
                    backup_job_size_bytes.add_metric(labels, float(job["BackupSizeInBytes"]))

        LOGGER.debug('querying Backup jobs')

        paginate(
            BACKUP.list_backup_jobs, observe, dict(ByCreatedAfter=datetime.datetime.now() - datetime.timedelta(1)),
        )

        yield backup_job_percent_done
        yield backup_job_size_bytes

        LOGGER.debug('finished querying Backup jobs')


    def get_backup_vaults(self):
        """
        {
            'BackupVaultList': [
                {
                    'BackupVaultName': 'string',
                    'BackupVaultArn': 'string',
                    'CreationDate': datetime(2015, 1, 1),
                    'EncryptionKeyArn': 'string',
                    'CreatorRequestId': 'string',
                    'NumberOfRecoveryPoints': 123
                },
            ],
            'NextToken': 'string'
        }
        """
        backup_vault_recovery_points = GaugeMetricFamily('aws_backup_vault_recovery_points', 'AWS Backup vault number of recovery points', labels=BACKUP_VAULT_LABELS)

        def observe(response):
            for vault in response.get("BackupVaultList", []):
                labels = [
                    get_account_id(),
                    strget(vault, 'BackupVaultName')
                ]

                backup_vault_recovery_points.add_metric(labels, vault["NumberOfRecoveryPoints"])

        LOGGER.debug('querying Backup vaults')

        paginate(BACKUP.list_backup_vaults, observe)

        yield backup_vault_recovery_points

        LOGGER.debug('finished querying Backup vaults')

# -*- coding: utf-8 -*-
