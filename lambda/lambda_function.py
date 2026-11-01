import json
import os
import re
import urllib.request
from datetime import datetime, timedelta, time

SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK", "")
NEW_RELIC_API_KEY = os.environ.get("NEW_RELIC_API_KEY")
ACCOUNT_ID = os.environ.get("ACCOUNT_ID")

NEW_RELIC_API = "https://api.newrelic.com/graphql"

# ✅ Policy Mapping (P1–P4)
POLICY_MAP = {
    "P1": [4500000],
    "P2": [5600000],
    "P3": [3450000],
    "P4": [10200000] 
}


def get_now_ist():
    return (datetime.utcnow() + timedelta(hours=5, minutes=30)).time()


# ✅ Mute windows (IST)
def is_mute_time(window):
    now_ist = get_now_ist()

    if window == "P1":   # 11:45 PM → 7:00 AM
        return now_ist >= time(23, 45) or now_ist <= time(7, 0)

    if window == "P2":   # 8:00 PM → 9:30 AM
        return now_ist >= time(20, 0) or now_ist <= time(9, 30)

    if window == "P3":   # 11:00 PM → 8:00 AM
        return now_ist >= time(23, 0) or now_ist <= time(8, 0)

    # P4 → always active (no mute)
    return False


def toggle_policy(policy_id, enable=True):
    try:
        query = f"""
        mutation {{
          alertsPolicyUpdate(
            accountId: {ACCOUNT_ID},
            id: {policy_id},
            policy: {{ enabled: {str(enable).lower()} }}
          ) {{
            id
            name
            enabled
          }}
        }}
        """

        req = urllib.request.Request(
            NEW_RELIC_API,
            data=json.dumps({"query": query}).encode(),
            headers={
                "Content-Type": "application/json",
                "API-Key": NEW_RELIC_API_KEY
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=10) as res:
            # 🆕 CHANGED: GraphQL returns HTTP 200 even when the mutation fails,
            # so check "errors" instead of assuming success.
            data = json.loads(res.read().decode())
            if data.get("errors"):
                print(f"Policy toggle FAILED for {policy_id}: {data['errors']}")
            else:
                print(f"Policy {policy_id} -> {'ENABLED' if enable else 'DISABLED'}")

    except Exception as e:
        print(f"Policy toggle failed for {policy_id}: {str(e)}")


# ✅ Enforce correct state every run
def manage_policies():
    now_ist = get_now_ist()

    for window, policies in POLICY_MAP.items():
        mute = is_mute_time(window)

        for policy in policies:
            toggle_policy(policy, enable=not mute)
            print(f"[{now_ist}] {window} -> {'DISABLED' if mute else 'ENABLED'}")


def utc_to_ist(value):
    if not value:
        return value

    try:
        v = str(value).replace('Z', '')
        dt = datetime.fromisoformat(v)
        ist = dt + timedelta(hours=5, minutes=30)
        return ist.strftime("%b %d, %Y %H:%M:%S IST")
    except Exception:
        return value


def highlight(text):
    if not text or text == "N/A":
        return "`N/A`"
    lines = str(text).split("\n")
    return "\n".join([f"`{line.strip()}`" for line in lines if line.strip()])


def extract_policy_name(raw_text):
    try:
        if "|" in raw_text:
            return raw_text.split("|", 1)[1].strip()
        return "Unknown"
    except Exception:
        return "Unknown"


# 🆕 NEW: find which window (P1/P2/P3/P4) an alert belongs to,
# from the policy name in "text", e.g. "... | P2 - Svc Critical / API Non-Critical"
def get_window_from_text(raw_text):
    match = re.search(r"\b(P[1-4])\b", extract_policy_name(raw_text or ""))
    return match.group(1) if match else None


# 🆕 NEW: a real New Relic alert always has "text" and attachment fields.
# Anything else (empty event, scheduler event, test invoke) must not go to Slack.
def is_valid_alert(body):
    if not isinstance(body, dict):
        return False
    text = str(body.get("text") or "").strip()
    attachments = body.get("attachments") or []
    has_fields = bool(attachments) and isinstance(attachments[0], dict) and bool(attachments[0].get("fields"))
    return bool(text) and has_fields


def format_payload(body):
    raw_text = body.get("text", "")
    attachments = body.get("attachments") or []
    fields = attachments[0].get("fields", []) if attachments else []

    entity = txn = opened = closed = "N/A"

    for f in fields:
        title = f.get("title", "")
        val = (f.get("value") or "").strip()

        if "Entity" in title:
            entity = val
        elif "Transaction" in title:
            txn = val
        elif "Opened" in title:
            opened = utc_to_ist(val)
        elif any(x in title for x in ["Closed", "Duration", "Ongoing"]):
            closed = utc_to_ist(val)

    is_resolved = "RESOLVED" in raw_text

    # fallback for closed time
    if is_resolved and (closed in ("N/A", "", "Still Open")):
        now_ist = datetime.utcnow() + timedelta(hours=5, minutes=30)
        closed = now_ist.strftime("%b %d, %Y %H:%M:%S IST")

    policy = extract_policy_name(raw_text)

    header = (
        f":white_check_mark: *RESOLVED - Throughput Restored* | {policy}"
        if is_resolved
        else f":rotating_light: *CRITICAL - Zero Throughput Detected* | {policy}"
    )

    return {
        "text": header,
        "attachments": [{
            "color": "#36a64f" if is_resolved else "#FF0000",
            "fields": [
                {"title": "📋 Entity Details", "value": highlight(entity), "short": False},
                {"title": "🔗 Transaction Name", "value": highlight(txn), "short": False},
                {"title": "🕒 Opened (IST)", "value": highlight(opened), "short": False},
                {
                    "title": "🔴 Closed (IST)" if is_resolved else "🕒 Ongoing (IST)",
                    "value": highlight(closed),
                    "short": False
                }
            ]
        }]
    }


def send_to_slack(payload):
    if not SLACK_WEBHOOK:
        print("Missing Slack webhook")
        return

    req = urllib.request.Request(
        SLACK_WEBHOOK,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=10) as res:
        print("Slack status:", res.status)


def lambda_handler(event, context):
    try:
        # 🆕 NEW: log the raw event so any odd invocation can be traced
        print("Incoming event:", json.dumps(event, default=str)[:2000])

        # ✅ EventBridge → policy toggle
        # 🆕 CHANGED: also accept EventBridge Scheduler and {"action": "sync_policies"}
        if isinstance(event, dict) and (
            event.get("source") in ("aws.events", "aws.scheduler")
            or event.get("action") == "sync_policies"
        ):
            manage_policies()
            return {"statusCode": 200, "body": "Policy sync complete"}

        # ✅ New Relic webhook → Slack
        body_str = event.get("body", event)
        body = json.loads(body_str) if isinstance(body_str, str) else body_str

        # 🆕 NEW: drop empty / non-alert events (these caused the "Unknown / N/A" Slack messages)
        if not is_valid_alert(body):
            print("Skipped: not a valid New Relic alert payload, nothing sent to Slack")
            return {"statusCode": 200, "body": "Skipped: invalid payload"}

        # 🆕 NEW: suppress alerts that arrive during that policy's mute window
        window = get_window_from_text(body.get("text", ""))
        if window and is_mute_time(window):
            print(f"Muted: {window} alert suppressed during mute window ({get_now_ist()} IST)")
            return {"statusCode": 200, "body": f"Muted: {window} in mute window"}

        payload = format_payload(body)
        send_to_slack(payload)

        return {"statusCode": 200, "body": "Notification Sent"}

    except Exception as e:
        print("Error:", str(e))
        return {"statusCode": 500, "body": str(e)}