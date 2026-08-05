---
name: security-secrets
description: Use when handling secrets, API keys, credentials, tokens, .env files, config files, security reviews, secret leaks, access control, redaction, rotation, or secure local/project setup.
---

# Security Secrets

## Overview

Use this skill to prevent accidental exposure of credentials and to handle suspected leaks conservatively. Treat secrets as compromised when they have been committed, pasted into chat, logged, or shared outside the intended secret store.

## Rules

- Never print full secret values in responses, logs, diffs, or examples.
- Use placeholders such as `sk-...REDACTED` or `YOUR_API_KEY`.
- Prefer environment variables, secret stores, CI/CD secret settings, or platform-managed credentials.
- Keep `.env` files out of git and provide `.env.example` with placeholders only.
- If a real secret is exposed, recommend rotation instead of relying only on deletion.

## Workflow

1. Identify where secrets live: `.env`, config files, code, logs, shell history, CI files, deployment dashboards, or committed history.
2. Check ignore rules and examples: `.gitignore`, `.env.example`, deployment docs, and CI secret references.
3. Remove hard-coded values from code and replace with configuration reads.
4. If committed, assess whether history rewrite is needed and tell the user to rotate the secret.
5. Verify with targeted searches for key patterns and known variable names.

## Common Checks

Search for terms like `api_key`, `secret`, `token`, `password`, `private_key`, `client_secret`, `.env`, `Authorization`, `Bearer`, and cloud provider key formats.

## Guardrails

Do not attempt to use, validate, or exfiltrate credentials. Do not send secrets to third-party services. When uncertain, redact first and ask for confirmation.
