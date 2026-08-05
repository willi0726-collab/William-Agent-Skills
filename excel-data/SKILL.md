---
name: excel-data
description: Use when working with spreadsheet data such as Excel, CSV, TSV, or XLSX files for cleaning, analysis, formulas, pivots, charts, reconciliation, validation, or data QA.
---

# Excel Data

## Overview

Use this skill to inspect spreadsheet files, preserve the source data, and produce source-backed analysis or cleaned outputs. Prefer structured spreadsheet libraries over ad hoc text parsing whenever the file format supports it.

## Workflow

1. Identify the file type, workbook sheets, headers, row counts, formulas, merged cells, hidden sheets, filters, and obvious encoding or locale issues.
2. Confirm the business question, output format, and success criteria before changing data.
3. Work from raw rows when possible. Do not rely only on screenshots, pivot totals, or pre-summarized exports if source tables exist.
4. Keep originals intact. Write cleaned or derived files as separate outputs unless the user explicitly asks to edit in place.
5. Validate totals, row counts, joins, date parsing, currency parsing, and formula preservation before reporting results.

## Common Tasks

- Clean CSV/XLSX exports: trim whitespace, normalize headers, split/merge columns, deduplicate, and standardize dates or currencies.
- Analyze data: group, filter, pivot, calculate KPIs, find outliers, reconcile totals, and explain drivers.
- Build workbook deliverables: add formulas, tables, charts, validation sheets, summary sheets, or review flags.
- Debug spreadsheet issues: broken formulas, inconsistent types, duplicate IDs, missing values, or mismatched totals.

## Output Standards

Report assumptions, formulas, filters, excluded rows, and any data quality issues that affect interpretation. For generated files, state the output path and the checks performed.

## Guardrails

Do not invent missing values. Do not overwrite source files without explicit confirmation. Treat private financial, customer, and operational data as sensitive.
