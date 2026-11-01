# New Relic Workflow Webhook Payload

## Purpose

This document describes the JSON payload configured in the New Relic Workflow notification destination.

The webhook forwards incident information to AWS API Gateway, which invokes the AWS Lambda function.

## Webhook JSON

```json
{
  "text": "{{#if closedAt}}✅ RESOLVED - Throughput Restored{{else}}🚨 CRITICAL - Zero Throughput Detected{{/if}} | {{#each accumulations.policyName}}{{escape this}}{{/each}}",
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

## Payload Fields

| Field | Description |
|---|---|
| text | Alert status and policy name |
| Entity Details | Affected service or application |
| Transaction Name | Affected API transaction |
| Opened | Incident creation timestamp |
| Ongoing | Current incident status or closure timestamp |

## Notification Types

- Critical: Zero Throughput Detected.
- Resolved: Throughput Restored.

## Processing

AWS Lambda validates the incoming webhook, extracts the incident details, converts timestamps to IST, formats the Slack message and sends the notification.
