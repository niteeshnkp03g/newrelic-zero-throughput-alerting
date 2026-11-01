# Policy Mute and Unmute Schedule

## 1. Overview

This document explains the priority-based New Relic alert-policy mute and unmute logic implemented inside AWS Lambda.

The Lambda function evaluates configured policy rules and time windows and updates the applicable New Relic alert policies through the New Relic API.

## 2. Priority Classification

The solution uses four priority categories:

| Priority | Service Criticality | API Criticality |
|---|---|---|
| P1 | Critical | Critical |
| P2 | Critical | Non-Critical |
| P3 | Non-Critical | Critical |
| P4 | Non-Critical | Non-Critical |

Each priority category is associated with its corresponding New Relic alert policy.

## 3. Mute and Unmute Logic

The mute/unmute functionality is implemented within the Python Lambda function.

The general processing flow is:

1. Lambda receives an invocation.
2. The function identifies the applicable event and policy information.
3. The function evaluates the configured mute/unmute rules.
4. It checks whether the applicable policy should be enabled or disabled.
5. When a policy update is required, Lambda calls the New Relic API.
6. The New Relic API updates the alert-policy status.

## 4. Policy Management

The Lambda implementation uses New Relic's alert-policy management API to update policy status.

The policy-management operation can enable or disable a policy based on the configured logic.

The actual policy mapping and time-window rules are maintained in the Lambda implementation.

## 5. Timezone Handling

The Lambda implementation includes IST timezone handling for policy-window evaluation.

The function uses UTC-to-IST conversion so that configured policy rules can be evaluated using Indian Standard Time.

## 6. Priority-Based Policy Behavior

The policy-management logic supports:

- P1 – Critical service and critical API.
- P2 – Critical service and non-critical API.
- P3 – Non-critical service and critical API.
- P4 – Non-critical service and non-critical API.

The actual mute/unmute behavior depends on the configured rules in the Lambda function.

## 7. Policy Mute/Unmute Flow

1. Lambda is invoked.
2. The policy-management logic identifies the applicable priority.
3. The configured time-window rule is evaluated.
4. The required policy action is determined.
5. Lambda communicates with the New Relic API if a status change is required.
6. The policy status is updated in New Relic.

## 8. Important Notes

- Policy mute/unmute logic is implemented inside AWS Lambda.
- API Gateway is used to receive and forward New Relic webhook requests.
- No Amazon EventBridge integration is included.
- Lambda must be invoked for its policy-management logic to execute.
- Actual policy IDs, credentials, and internal schedules must not be published in a public repository.
