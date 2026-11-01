# Deployment and Configuration Guide

## Overview

This document describes the production configuration of the New Relic zero-throughput alerting solution.

## New Relic Configuration

1. Configure service-based NRQL alert conditions.
2. Enable signal-loss detection.
3. Associate the conditions with the appropriate P1–P4 policies.
4. Configure the New Relic notification destination.
5. Configure the webhook payload.
6. Associate the destination with the appropriate workflows.

## AWS Lambda Configuration

Function name:

`newrelic-throughput-alert`

Handler:

`lambda_function.lambda_handler`

Runtime:

Use the Python runtime configured by the deployed production function.

Environment variables:

- NEW_RELIC_API_KEY
- NR_ACCOUNT_ID (or the exact variable name used by the deployed code)
- SLACK_WEBHOOK

Policy IDs are configured through the Lambda policy mapping.

## API Gateway

API Gateway receives New Relic webhook requests and invokes the Lambda function.

## EventBridge Scheduler

EventBridge Scheduler periodically invokes Lambda to synchronize policy states according to the configured mute schedule.

## Monitoring

AWS CloudWatch Logs are used to inspect Lambda execution, webhook processing and policy synchronization.

## Security

Never store actual API keys, Slack webhook URLs or AWS credentials in GitHub.

This document describes the existing production implementation. Perform configuration changes only through the approved production change process.
