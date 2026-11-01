# Setup Guide – New Relic Zero Throughput Alerting

## 1. Overview

This guide explains the main configuration steps for the New Relic Zero Throughput Alerting solution.

The integration uses:

- New Relic APM
- NRQL alert conditions
- New Relic workflows
- AWS API Gateway
- AWS Lambda
- Slack notifications

## 2. Prerequisites

Before starting, ensure you have:

- Access to a New Relic account.
- Permission to configure New Relic alert conditions and workflows.
- Access to an AWS account.
- Permission to configure API Gateway and Lambda.
- A Slack incoming webhook URL.
- A New Relic API key with the required alert-policy permissions.
- Python code and dependencies required by the Lambda function.

## 3. Configure New Relic Monitoring

1. Open your New Relic account.
2. Navigate to the alerting section.
3. Create or review the NRQL alert condition for throughput monitoring.
4. Configure the condition to identify zero-throughput scenarios.
5. Configure the required threshold and evaluation settings.
6. Save the alert condition.

Use an appropriate NRQL query for the application and transaction being monitored.

## 4. Configure New Relic Workflow

1. Open New Relic Workflows.
2. Create or update a workflow for the zero-throughput alert condition.
3. Configure the workflow trigger.
4. Add a webhook destination.
5. Provide the AWS API Gateway endpoint as the destination URL.
6. Configure the required webhook payload.
7. Save the workflow.

The workflow forwards alert information to API Gateway.

Refer to [Workflow Payload Documentation](workflow-payload.md) for the payload structure.

## 5. Configure AWS Lambda

1. Open the AWS Lambda console.
2. Create or select the Lambda function.
3. Configure the Python runtime required by the implementation.
4. Upload the Lambda deployment package or code.
5. Configure the required execution permissions.
6. Verify that the Lambda function can access the required New Relic and Slack services.

The Lambda function is responsible for:

- Processing incoming webhook events.
- Validating alert payloads.
- Extracting alert and policy information.
- Applying the configured policy mute/unmute logic.
- Communicating with the New Relic API when policy updates are required.
- Sending notifications to Slack.

## 6. Configure Lambda Environment Variables

Configure the environment variables expected by the deployed Lambda code.

| Variable | Description |
|---|---|
| `SLACK_WEBHOOK` | Slack incoming webhook URL |
| `NEW_RELIC_API_KEY` | New Relic API key |
| `ACCOUNT_ID` | New Relic account identifier |

Use the exact variable names expected by your Lambda implementation.

Do not use real credentials in documentation, source-control files, or screenshots.

## 7. Configure API Gateway

1. Open the AWS API Gateway console.
2. Create or select the API used for the webhook integration.
3. Configure the required HTTP method and resource path.
4. Configure the integration with the Lambda function.
5. Enable Lambda invocation permissions for API Gateway.
6. Deploy the API to the required stage.
7. Copy the API endpoint.

The API Gateway endpoint is configured as the webhook destination in the New Relic workflow.

## 8. Connect API Gateway with New Relic

1. Copy the deployed API Gateway endpoint.
2. Open the New Relic workflow configuration.
3. Add or edit the webhook destination.
4. Paste the API Gateway endpoint.
5. Verify the HTTP method and payload configuration.
6. Save the workflow.

When the alert condition is triggered, New Relic sends the webhook request to API Gateway, which forwards it to Lambda.

## 9. Configure Slack Notifications

1. Create or select the Slack incoming webhook integration.
2. Copy the webhook URL.
3. Configure it in the Lambda environment using `SLACK_WEBHOOK`.
4. Verify that Lambda can send a test notification.

Never publish the actual Slack webhook URL.

## 10. Configure Policy Mute/Unmute Logic

The policy mute/unmute functionality is implemented inside the Lambda code.

The function evaluates the configured priority and time-window rules and updates the applicable New Relic alert policies through the New Relic API.

Refer to [Policy Mute and Unmute Documentation](policy-mute-schedule.md) for more information.

## 11. Validate the Integration

Perform testing with non-production test data.

Verify the following:

- New Relic detects the zero-throughput condition.
- The New Relic workflow is triggered.
- API Gateway receives the webhook request.
- API Gateway invokes Lambda successfully.
- Lambda processes the incoming payload.
- Policy-management logic behaves as expected.
- Slack receives the expected notification.

## 12. Troubleshooting

If any step fails, review:

- New Relic workflow execution details.
- API Gateway request and integration logs.
- Lambda CloudWatch logs.
- Lambda environment-variable configuration.
- New Relic API authentication and permissions.
- Slack webhook configuration.

Refer to [Troubleshooting Documentation](troubleshooting.md).

## 13. Important Notes

- API Gateway acts as the bridge between New Relic and Lambda.
- Lambda contains the alert-processing and policy mute/unmute logic.
- No Amazon EventBridge integration is included in this setup.
- Lambda executes its logic when invoked.
- Test changes in a non-production environment before applying them to production.
- Never commit production credentials, policy IDs, or internal service information to a public repository.
