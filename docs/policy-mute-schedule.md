# New Relic Alert Policy Mute Schedule

## Overview

The Lambda function manages four New Relic alert policies based on their configured mute windows.

All schedule timings use Indian Standard Time (IST).

## Policy Mapping

| Priority | Policy ID | Description |
|---|---:|---|
| P1 | 7207794 | Service Critical / API Critical |
| P2 | 7284556 | Service Critical / API Non-Critical |
| P3 | 7304198 | Service Non-Critical / API Critical |
| P4 | 7304289 | Service Non-Critical / API Non-Critical |

## Mute Windows

| Policy | Start | End |
|---|---|---|
| P1 | 11:45 PM | 07:00 AM |
| P2 | 08:00 PM | 09:30 AM |
| P3 | 11:00 PM | 08:00 AM |
| P4 | No mute | Always active |

## Policy Management

The Lambda function checks the current IST time and determines whether each policy should be enabled or disabled.

New Relic GraphQL API is used to update the policy state.

AWS EventBridge Scheduler invokes Lambda for periodic policy synchronization.

## Important

The mute mechanism disables the entire alert policy. Policies should be dedicated to the intended zero-throughput alert conditions to avoid unintentionally suppressing unrelated alerts.
