# New Relic Workflow Webhook Payload

## 1. Overview

This document describes the webhook payload used by the New Relic workflow to send zero-throughput alert information to AWS Lambda through API Gateway.

The integration flow is:

**New Relic Workflow → AWS API Gateway → AWS Lambda**

Lambda processes the incoming payload and handles the configured alert and policy-management logic.

## 2. Webhook Configuration

Configure a webhook destination in the New Relic workflow.

| Setting | Description |
|---|---|
| Destination | AWS API Gateway endpoint |
| HTTP Method | POST |
| Content Type | application/json |
| Receiver | AWS Lambda through API Gateway |

Use the deployed API Gateway endpoint as the webhook destination.

## 3. Example Webhook Payload

The following is a generic example of the payload structure:

```json
{
  "text": "{{#if closedAt}}RESOLVED - Throughput Restored{{else}}ALERT - Zero Throughput Detected{{/if}} | {{#each accumulations.policyName}}{{escape this}}{{/each}}",
  "attachments": [
    {
      "fields": [
        {
          "title": "Entity Details",
          "value": "{{escape accumulations.metadata_entity_name.[0]}}"
        },
        {
          "title": "Transaction Name",
          "value": "{{escape accumulations.targetName.[0]}}"
        },
        {
          "title": "Opened",
          "value": "{{issueCreatedAt}}"
        },
        {
          "title": "Ongoing",
          "value": "{{#if closedAt}}{{issueClosedAt}}{{else}}Still Open{{/if}}"
        }
      ]
    }
  ]
}
```

**Note:** This is a generic example based on the New Relic workflow template. Confirm that the fields match the actual workflow configuration and the Lambda payload parser before using it.

## 4. Payload Field Description

| Field | Purpose |
|---|---|
| `text` | Alert or resolution message |
| `attachments` | Additional alert information |
| `fields` | Collection of alert details |
| `title` | Name of the displayed field |
| `value` | Value associated with the field |
| `issueCreatedAt` | Alert creation timestamp |
| `issueClosedAt` | Alert resolution timestamp |
| `accumulations.policyName` | Associated alert-policy information |
| `accumulations.metadata_entity_name` | Monitored entity information |
| `accumulations.targetName` | Transaction or target information |
| `closedAt` | Used by the template to distinguish alert and resolution events |

## 5. Alert and Resolution Handling

The workflow template uses `closedAt` to distinguish between two conditions:

**Alert event**
- The alert is not resolved.
- The message indicates that zero throughput has been detected.
- The event contains the available entity, transaction, and policy information.

**Resolution event**
- The alert has been resolved.
- The message indicates that throughput has been restored.
- The resolution timestamp is included when available.

## 6. Request Processing

1. New Relic evaluates the alert condition.
2. The workflow generates the webhook payload.
3. The webhook is sent to the API Gateway endpoint.
4. API Gateway forwards the request to AWS Lambda.
5. Lambda validates and processes the payload.
6. Lambda executes the relevant alert and policy-management logic.
7. The notification is formatted and sent to Slack when applicable.

## 7. Payload Validation

When testing the integration, verify:

- The request uses the expected JSON structure.
- The alert message is populated correctly.
- Policy information is available.
- Entity and transaction information are populated when available.
- Creation and resolution timestamps are handled correctly.
- Lambda can parse the incoming payload.

## 8. Security Considerations

- Do not include API keys or Slack webhook URLs in the payload.
- Do not publish real production entity names or transaction names.
- Use generic sample values in public documentation.
- Avoid exposing internal account or policy identifiers.

## 9. Related Documentation

- [Architecture](architecture.md)
- [Setup Guide](setup-guide.md)
- [Policy Mute and Unmute Schedule](policy-mute-schedule.md)
- [Troubleshooting](troubleshooting.md)
