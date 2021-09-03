# AWS Prometheus Exporter

[![CircleCI](https://circleci.com/gh/ClarkSource/aws-exporter/tree/master.svg?style=shield)](https://circleci.com/gh/ClarkSource/aws-exporter/tree/master)
[![PyPi version](https://pypip.in/v/aws-exporter/badge.png)](https://pypi.org/project/aws-exporter/)
[![PyPi downloads](https://pypip.in/d/aws-exporter/badge.png)](https://pypi.org/project/aws-exporter/)
[![CLARK Open Source](https://img.shields.io/badge/CLARK-Open%20Source-%232B6CDE.svg)](https://www.clark.de/de/jobs)

Prometheus exporter for generic AWS metrics.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Metrics](#metrics)
  - [AWS Backup](#aws-backup)
  - [AWS SNS](#aws-sns)
  - [AWS EC2 AMIs](#aws-ec2-amis)
    - [configuration](#configuration)
  - [AWS EC2 Instances](#aws-ec2-instances)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Installation

```bash
$ git clone git@github.com:ClarkSource/aws-exporter.git
$ cd aws-exporter
$ pip install --user --upgrade .
```

## Usage

Just start the exporter with read only credentials on AWS. This is using boto, so the usual rules for passing credentials apply.

```bash
$ aws-exporter
```

The exporter should be exposed on port `8000`

## Configuration

`AWS_EXPORTER_LOG_LEVEL` - [debug,info,warning,error,critical,fatal]

## Metrics

### AWS Backup

* aws_backup_job_collector_success
* aws_backup_job_size_bytes
* aws_backup_job_percent_done
* aws_backup_vault_collector_success
* aws_backup_vault_recovery_points

### AWS SNS

* sns_platform_application_collector_success
* sns_platform_application_enabled
* sns_platform_application_cert_expiry

### AWS EC2 AMIs

* ec2_ami_collector_success
* ec2_ami_creation_date

#### configuration

`AWS_EXPORTER_EC2_AMI_OWNERS` - additional AMI owners, comma separated.

### AWS EC2 Instances

* ec2_instance_collector_success
* ec2_instance_creation_date
