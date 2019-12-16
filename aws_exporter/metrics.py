# -*- coding: utf-8 -*-
# ISC License
#
# Copyright 2019 FL Fintech E GmbH
#
# Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from prometheus_client import Gauge

COMMON_LABELS = ['creation_date']

###############################################################################
# AWS Backup

BACKUP_JOB_LABELS = COMMON_LABELS + [
    'completion_date',
    'backup_job_id',
    'backup_job_state',
    'backup_rule_id',
    'backup_plan_id',
    'backup_vault_name',
]

BACKUP_JOB_SIZE_BYTES = Gauge(
    'aws_backup_job_size_bytes', 'AWS Backup job size in bytes', BACKUP_JOB_LABELS)
BACKUP_JOB_PERCENT_DONE = Gauge(
    'aws_backup_job_percent_done', 'AWS Backup job percent done', BACKUP_JOB_LABELS)

BACKUP_VAULT_LABELS = COMMON_LABELS + ['backup_vault_name']

BACKUP_VAULT_RECOVERY_POINTS = Gauge(
    'aws_backup_recovery_points', 'AWS Backup vault number of recovery points', BACKUP_VAULT_LABELS)