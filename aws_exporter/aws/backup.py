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
from aws_exporter.metrics import (BACKUP_JOB_COLLECTOR_SUCCESS,
                                  BACKUP_JOB_PERCENT_DONE,
                                  BACKUP_JOB_SIZE_BYTES,
                                  BACKUP_VAULT_COLLECTOR_SUCCESS,
                                  BACKUP_VAULT_RECOVERY_POINTS)
from aws_exporter.aws.sts import get_account_id
from aws_exporter.util import paginate, success_metric

BACKUP = boto3.client("backup")
LOGGER = logging.getLogger(__name__)


@success_metric(BACKUP_JOB_COLLECTOR_SUCCESS)
def get_backup_jobs():
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

    def observe(response):
        for job in response.get("BackupJobs", []):
            labels = [
                get_account_id(),
                job["CreationDate"],
                job["CompletionDate"],
                job["BackupJobId"],
                job["State"],
                job["CreatedBy"]["BackupRuleId"],
                job["CreatedBy"]["BackupPlanId"],
                job["BackupVaultName"],
            ]

            BACKUP_JOB_PERCENT_DONE.labels(*labels).set(float(job["PercentDone"]))

            if "BackupSizeInBytes" in job:
                BACKUP_JOB_SIZE_BYTES.labels(*labels).set(float(job["BackupSizeInBytes"]))

    LOGGER.debug('querying Backup jobs')

    paginate(
        BACKUP.list_backup_jobs, observe, dict(ByCreatedAfter=datetime.datetime.now() - datetime.timedelta(1)),
    )

    LOGGER.debug('finished querying Backup jobs')


@success_metric(BACKUP_VAULT_COLLECTOR_SUCCESS)
def get_backup_vaults():
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

    def observe(response):
        for vault in response.get("BackupVaultList", []):
            labels = [
                get_account_id(),
                vault["BackupVaultName"],
            ]

            BACKUP_VAULT_RECOVERY_POINTS.labels(*labels).set(vault["NumberOfRecoveryPoints"])

    LOGGER.debug('querying Backup vaults')

    paginate(BACKUP.list_backup_vaults, observe)

    LOGGER.debug('finished querying Backup vaults')
