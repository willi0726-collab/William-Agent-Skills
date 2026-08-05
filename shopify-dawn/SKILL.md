---
name: shopify-dawn
description: Use when editing, debugging, customizing, or explaining Shopify Dawn theme Liquid, JSON templates, sections, blocks, snippets, CSS, JavaScript, metafields, product pages, collection pages, cart, or checkout-adjacent storefront behavior.
---

# Shopify Dawn

## Overview

Use this skill for Dawn theme work that should follow Shopify theme conventions and the existing store's structure. Keep changes scoped to the relevant template, section, snippet, asset, or locale file.

## Workflow

1. Inspect the current theme structure before editing: `templates/`, `sections/`, `snippets/`, `assets/`, `locales/`, `config/settings_schema.json`, and `config/settings_data.json` when present.
2. Identify whether the task belongs in a JSON template, reusable section, block setting, snippet, CSS asset, JavaScript asset, or metafield-driven content.
3. Match Dawn's existing Liquid, schema, CSS, and JavaScript patterns. Prefer section settings and metafields over hard-coded store content.
4. Keep storefront copy translatable when the theme already uses locale files.
5. Verify with the narrowest useful check: `shopify theme check`, local preview, browser screenshot, or targeted Liquid/CSS review.

## Common Tasks

- Add or adjust product page sections, trust badges, accordions, tabs, media layouts, or variant-related messaging.
- Customize collection cards, filtering, sorting, banners, menus, headers, footers, and cart drawer content.
- Wire product, variant, collection, or metaobject metafields into theme output.
- Fix Dawn layout, spacing, responsive behavior, broken schema, or JavaScript interaction issues.

## Guardrails

Do not edit checkout behavior unless the user is using supported Shopify extension points. Do not hard-code secrets, private app tokens, or admin API keys in theme files. Avoid broad CSS resets and unrelated theme cleanup.
