# System Architecture

## Overview

The solution provides service-based API zero-throughput monitoring using New Relic and automated Slack notifications through AWS serverless services.

## Architecture Flow

1. New Relic APM collects application transaction data.
2. NRQL alert conditions monitor individual API endpoints.
3. Signal-loss detection identifies missing transaction data.
4. New Relic alert policies classify alerts into P1–P4.
5. New Relic Workflows generate webhook notifications.
6. AWS API Gateway receives the webhook.
7. AWS Lambda validates and processes the payload.
8. Lambda applies configured notification mute rules.
9. Incident timestamps are converted to IST.
10. Formatted notifications are delivered to Slack.

## Policy Synchronization

AWS EventBridge Scheduler invokes Lambda periodically.

Lambda evaluates the configured P1–P4 mute windows and updates the corresponding New Relic policy states through the GraphQL API.

## Incident Lifecycle

### Critical

Zero throughput is detected and a New Relic incident is opened. The webhook is processed and a critical notification is delivered to Slack.

### Resolved

When New Relic resolves the incident, a recovery notification is processed and delivered to Slack.

## Components

- New Relic APM
- NRQL
- New Relic Alerts and Workflows
- AWS API Gateway
- AWS Lambda
- AWS EventBridge Scheduler
- AWS CloudWatch
- Slack Incoming Webhook
