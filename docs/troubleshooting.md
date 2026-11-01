# Troubleshooting Guide

## Slack Notification Not Received

Check:
- New Relic Workflow execution.
- API Gateway request logs.
- Lambda execution logs.
- Slack webhook configuration.

## Lambda Execution Failure

Check:
- CloudWatch Logs.
- Lambda timeout.
- Environment variables.
- Incoming event structure.

## Incorrect Timestamp

Check:
- Incoming New Relic timestamp.
- UTC to IST conversion.
- Timestamp format.

## Policy Not Enabling or Disabling

Check:
- New Relic API key.
- New Relic account ID.
- Policy ID.
- GraphQL API response.
- EventBridge Scheduler execution.

## Invalid Slack Notification

Check:
- Incoming webhook JSON.
- Entity name.
- Transaction name.
- Incident state.
- Required attachment fields.

## Duplicate Notifications

Check:
- New Relic workflow triggers.
- Duplicate webhook deliveries.
- Lambda event processing.

## Important

Do not change production alert conditions or policy settings while troubleshooting without following the approved change process.
