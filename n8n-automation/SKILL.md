---
name: n8n-automation
description: Use when designing, building, reviewing, or debugging n8n workflows, nodes, credentials, triggers, webhooks, schedules, HTTP requests, data transforms, error handling, or automation handoffs.
---

# n8n Automation

## Overview

Use this skill to design n8n workflows that are explicit about triggers, data shape, credentials, retries, and failure handling. Prefer simple, observable workflows over clever node chains.

## Workflow

1. Define the trigger, input schema, output target, success criteria, and failure behavior.
2. Choose the minimum node set: trigger, fetch/receive, transform, branch, action, notify, and log.
3. Document data contracts between nodes, including required fields, optional fields, and example payloads.
4. Handle credentials through n8n credential storage or environment variables. Never put secrets in workflow JSON.
5. Add retry, deduplication, rate-limit, and error paths when the external system can fail or repeat events.
6. When producing workflow JSON, keep it importable and call out placeholders the user must fill.

## Review Checklist

- Trigger cannot accidentally run at the wrong cadence or on the wrong data.
- Webhook responses are explicit and do not leak sensitive payloads.
- HTTP nodes include method, URL, headers, pagination, timeout, and error handling where needed.
- Code nodes are short and only used when native nodes are insufficient.
- Notifications include enough context to debug failures without exposing secrets.

## Guardrails

Do not execute live automations, send emails, charge cards, modify production records, or call destructive APIs unless the user explicitly confirms the exact action.
