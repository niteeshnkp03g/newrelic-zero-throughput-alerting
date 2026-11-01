# New Relic Zero Throughput Alerting

## Overview

This project implements a zero-throughput alerting solution using New Relic, AWS API Gateway, AWS Lambda, and Slack.

The solution detects when a monitored application or transaction experiences zero throughput and sends alert notifications to Slack through an automated workflow.

AWS Lambda processes incoming webhook events, manages the configured New Relic alert-policy mute/unmute logic, and handles Slack notifications.

The project also supports priority-based policy management for P1, P2, P3, and P4 alert categories.

## Technologies Used

- **New Relic:** APM monitoring, NRQL alert conditions, and alert workflows.
- **AWS API Gateway:** Receives webhook requests from New Relic and forwards them to Lambda.
- **AWS Lambda:** Processes webhook events, applies policy mute/unmute logic, and handles notifications.
- **Python:** Lambda application logic.
- **Slack:** Receives alert and resolution notifications.

## Architecture

The solution follows this flow:

1. New Relic monitors application throughput.
2. A zero-throughput condition triggers a New Relic alert.
3. The New Relic workflow sends a webhook request to AWS API Gateway.
4. API Gateway forwards the request to AWS Lambda.
5. Lambda processes the incoming event and applies the configured policy logic.
6. Lambda interacts with the New Relic API when policy updates are required.
7. Alert notifications are sent to Slack.

### Architecture Diagram

![Zero Throughput Alerting Architecture](assets/architecture-diagram.png)

## Table of Contents

- [Features](#features)
- [Repository Structure](#repository-structure)
- [Lambda Processing Flow](#lambda-processing-flow)
- [Priority Classification](#priority-classification)
- [Policy Mute and Unmute Logic](#policy-mute-and-unmute-logic)
- [New Relic Workflow Payload](#new-relic-workflow-payload)
- [Environment Variables](#environment-variables)
- [Setup Guide](#setup-guide)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)
- [Resume Project Description](#resume-project-description)

## Features

- Zero-throughput monitoring using New Relic.
- NRQL-based alert conditions.
- New Relic workflow integration with AWS API Gateway.
- Webhook processing through AWS Lambda.
- Priority-based alert-policy management (P1–P4).
- Lambda-based policy mute/unmute logic.
- Slack notifications for alert and resolution events.
- IST timezone handling for configured policy windows.
- Centralized alert processing and policy management.

## Repository Structure

```text
newrelic-zero-throughput-alerting/
│
├── README.md
│
├── assets/
│   ├── architecture-diagram.png
│   ├── lambda-processing-flow.png
│   └── policy-mute-schedule.png
│
├── docs/
│   ├── architecture.md
│   ├── policy-mute-schedule.md
│   ├── setup-guide.md
│   ├── troubleshooting.md
│   └── workflow-payload.md
│
├── lambda/
│   └── lambda_function.py
│
└── screenshots/
```

## Lambda Processing Flow

AWS Lambda is responsible for processing incoming events and executing the configured application logic.

The main processing responsibilities include:

- Receiving webhook events forwarded by API Gateway.
- Validating incoming alert payloads.
- Extracting alert and policy information.
- Identifying the applicable priority category.
- Evaluating the configured mute/unmute conditions.
- Updating New Relic alert policies through the New Relic API when required.
- Formatting alert messages.
- Sending notifications to Slack.

### Lambda Processing Diagram

![Lambda Processing Flow](assets/lambda-processing-flow.png)

## Priority Classification

The solution uses four priority categories:

| Priority | Service Criticality | API Criticality |
|---|---|---|
| P1 | Critical | Critical |
| P2 | Critical | Non-Critical |
| P3 | Non-Critical | Critical |
| P4 | Non-Critical | Non-Critical |

The priority classification determines which alert policy is managed by the Lambda logic.

## Policy Mute and Unmute Logic

The mute/unmute functionality is implemented inside AWS Lambda.

Lambda evaluates the configured policy rules and time windows and interacts with the New Relic API to enable or disable the applicable alert policies.

The policy-management logic supports the P1, P2, P3, and P4 priority categories.

The configured time windows and policy behavior are documented here:

[Policy Mute and Unmute Documentation](docs/policy-mute-schedule.md)

**Note:** The policy-management logic runs when Lambda is invoked with the relevant event. This project documentation does not assume an EventBridge integration.

## New Relic Workflow Payload

New Relic workflows send alert information to the API Gateway endpoint.

The payload contains information used by Lambda to identify and process the alert, including:

- Alert status.
- Policy information.
- Entity details.
- Transaction information.
- Alert creation and resolution timestamps.

See the complete payload documentation:

[New Relic Workflow Payload](docs/workflow-payload.md)

## Environment Variables

Configure the Lambda environment variables according to the names used by the deployed Lambda code.

| Variable | Purpose |
|---|---|
| `SLACK_WEBHOOK` | Slack incoming webhook used for notifications |
| `NEW_RELIC_API_KEY` | New Relic API key used for policy management |
| `ACCOUNT_ID` | New Relic account identifier used by the Lambda code |

**Security:** Never commit actual API keys, Slack webhook URLs, account identifiers, or policy IDs to a public GitHub repository. Use placeholders in examples.

## Setup Guide

Follow the detailed setup instructions in:

[Setup Guide](docs/setup-guide.md)

The setup documentation covers:

1. New Relic alert-condition configuration.
2. New Relic workflow configuration.
3. AWS API Gateway configuration.
4. AWS Lambda deployment.
5. Lambda environment configuration.
6. API Gateway and Lambda integration.
7. Slack notification configuration.
8. Testing the webhook integration.

## Testing

Validate the solution using non-production test data before making changes to any production alert policies.

Recommended checks:

- Verify that the New Relic alert condition detects zero throughput.
- Verify that the New Relic workflow sends the webhook.
- Verify that API Gateway receives the request.
- Verify that Lambda processes the incoming payload.
- Verify that the configured policy logic behaves as expected.
- Verify that Slack receives the notification.
- Verify alert resolution handling.

## Troubleshooting

For common issues and debugging steps, refer to:

[Troubleshooting Guide](docs/troubleshooting.md)

Common areas to investigate include:

- New Relic workflow webhook configuration.
- API Gateway endpoint and integration.
- Lambda execution errors and CloudWatch logs.
- Lambda environment variables.
- New Relic API authentication and permissions.
- Slack webhook configuration.
- Alert payload format and policy mapping.

## Future Enhancements

- Add more detailed alert-processing metrics.
- Improve error handling and retry mechanisms.
- Add automated testing for webhook payloads.
- Improve notification formatting.
- Extend support for additional alert categories.

## Resume Project Description

**New Relic Zero Throughput Alerting Automation**

- Implemented a zero-throughput alerting solution using New Relic APM, NRQL alert conditions, AWS API Gateway, AWS Lambda, and Slack.
- Integrated New Relic alert workflows with AWS Lambda through API Gateway for automated webhook processing.
- Developed Python-based Lambda logic to process alert events and manage priority-based New Relic policy mute/unmute operations.
- Integrated Slack notifications to communicate alert and resolution events.
