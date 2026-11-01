# Troubleshooting – New Relic Zero Throughput Alerting

## 1. Overview

This document describes common issues that may occur in the New Relic Zero Throughput Alerting integration and provides steps to investigate them.

The solution uses New Relic, AWS API Gateway, AWS Lambda, the New Relic API, and Slack.

## 2. New Relic Alert Not Triggering

**Possible causes:**
- Incorrect NRQL query.
- Alert threshold configuration issue.
- Incorrect evaluation window.
- No matching application or transaction data.
- Alert condition is not enabled.

**Troubleshooting steps:**

1. Open the New Relic alert condition.
2. Review the NRQL query.
3. Verify that the query returns the expected data.
4. Check the threshold and evaluation settings.
5. Confirm that the alert condition is enabled.
6. Review the alert condition evaluation details.

## 3. New Relic Workflow Not Triggering

**Possible causes:**
- Incorrect workflow trigger configuration.
- Alert condition is not associated with the workflow.
- Workflow is disabled.
- Webhook destination is incorrectly configured.

**Troubleshooting steps:**

1. Open the New Relic workflow.
2. Verify the trigger configuration.
3. Check whether the relevant alert condition matches the workflow.
4. Verify that the workflow is enabled.
5. Review workflow execution details.

## 4. API Gateway Not Receiving Webhook Requests

**Possible causes:**
- Incorrect API endpoint.
- Incorrect HTTP method or resource path.
- API deployment issue.
- Incorrect New Relic webhook destination.

**Troubleshooting steps:**

1. Open AWS API Gateway.
2. Verify the deployed API and stage.
3. Check the resource path and HTTP method.
4. Confirm that the New Relic workflow uses the correct endpoint.
5. Review API Gateway access or execution logs, if enabled.

## 5. API Gateway Not Invoking Lambda

**Possible causes:**
- Incorrect Lambda integration.
- Missing Lambda invocation permission.
- Incorrect API Gateway deployment.
- Integration configuration issue.

**Troubleshooting steps:**

1. Open the API Gateway integration settings.
2. Verify that the correct Lambda function is selected.
3. Check the Lambda invocation permission.
4. Confirm that the API is deployed.
5. Review API Gateway logs for integration errors.

## 6. Lambda Function Errors

**Possible causes:**
- Python runtime errors.
- Invalid incoming payload.
- Missing environment variables.
- Incorrect deployment package.
- Unexpected event structure.

**Troubleshooting steps:**

1. Open the AWS Lambda console.
2. Select the relevant function.
3. Open the Monitor section.
4. Review the CloudWatch logs.
5. Identify the error message and traceback.
6. Verify the incoming event structure.
7. Check the required environment variables.

## 7. New Relic API Errors

**Possible causes:**
- Invalid API key.
- Incorrect account identifier.
- Insufficient API permissions.
- Invalid policy identifier.
- New Relic API request failure.

**Troubleshooting steps:**

1. Verify that the Lambda function has the required New Relic API key.
2. Confirm that the account identifier is correct.
3. Check that the API key has the required permissions.
4. Verify the policy mapping used by the Lambda function.
5. Review Lambda logs for New Relic API response errors.

Never print API keys or other credentials in application logs.

## 8. Policy Mute/Unmute Not Working

**Possible causes:**
- Incorrect policy mapping.
- Incorrect time-window configuration.
- Timezone conversion issue.
- New Relic API authentication failure.
- Lambda policy-management logic error.

**Troubleshooting steps:**

1. Review the policy-management logic in Lambda.
2. Verify the priority-to-policy mapping.
3. Check the configured mute/unmute rules.
4. Verify the UTC-to-IST conversion.
5. Review the New Relic API response.
6. Check CloudWatch logs for policy-management errors.

The mute/unmute logic is implemented inside Lambda. No EventBridge integration is assumed.

## 9. Slack Notifications Not Received

**Possible causes:**
- Invalid Slack webhook URL.
- Missing `SLACK_WEBHOOK` environment variable.
- Incorrect notification payload.
- Slack webhook request failure.
- Network connectivity issue.

**Troubleshooting steps:**

1. Verify the `SLACK_WEBHOOK` Lambda environment variable.
2. Confirm that the webhook is valid.
3. Review the Slack request and response handling in Lambda.
4. Check CloudWatch logs for notification errors.
5. Verify that the formatted notification payload is valid.

Never publish the actual Slack webhook URL.

## 10. Timezone-Related Issues

**Possible causes:**
- Incorrect UTC-to-IST conversion.
- Incorrect time-window configuration.
- Unexpected timezone assumptions.

**Troubleshooting steps:**

1. Review the timezone conversion function.
2. Confirm that IST is handled consistently.
3. Check the configured time-window boundaries.
4. Validate the expected policy behavior using test data.

## 11. General Debugging Checklist

When investigating an issue, check the components in this order:

1. New Relic alert condition.
2. New Relic workflow execution.
3. API Gateway request and integration.
4. Lambda invocation and CloudWatch logs.
5. New Relic API response.
6. Slack webhook response.

This helps identify which part of the integration is failing.

## 12. Security Notes

- Never expose API keys, Slack webhook URLs, or account identifiers.
- Avoid logging sensitive request information.
- Do not publish production policy IDs or internal service names.
- Test policy changes in a non-production environment before applying them to production.

## 13. Architecture Reminder

The integration follows this flow:

**New Relic → API Gateway → AWS Lambda → New Relic API / Slack**

API Gateway receives and forwards webhook requests. Lambda handles alert processing and policy mute/unmute logic.
