---
name: amazon-ads-optimizer
description: Use when analyzing Amazon Ads, Sponsored Products, Sponsored Brands, Sponsored Display, search term, targeting, campaign, keyword, ASIN, placement, budget, ACOS, TACOS, CPC, CTR, CVR, bid, negative keyword, harvesting, or advertising report CSV/XLSX files to produce optimization recommendations.
---

# Amazon Ads Optimizer

## Overview

Use this skill to turn Amazon Ads exports into conservative, reviewable optimization actions: bid changes, negative keywords, search-term harvesting, ASIN/category expansion, and campaign budget moves.

Never directly change live Amazon Ads or Seller Central settings unless the user explicitly asks and confirms the exact action. Default to producing a recommendations table the user can review.

## Quick Start

1. Inspect the provided files and identify report type: search term, targeting/keyword, campaign, budget, advertised product, placement, or mixed export.
2. Prefer source-backed calculations from raw rows. Do not rely only on pivot totals or screenshots when raw CSV/XLSX exists.
3. Run `scripts/analyze_ads_report.py` for a first-pass recommendations CSV when the file is tabular.
4. Review the output for business context: product margin, launch phase, ranking goals, branded terms, seasonality, coupon/deal state, inventory, and account risk.
5. Present recommendations grouped by action: pause/negative, bid down, bid up, harvest/expand, budget increase, budget decrease, and investigate.

Example:

```powershell
python C:\Users\ZhuanZ\.codex\skills\amazon-ads-optimizer\scripts\analyze_ads_report.py `
  --input C:\path\amazon_ads_report.csv `
  --output C:\path\amazon_ads_recommendations.csv `
  --target-acos 0.30
```

## Inputs

Accept CSV/XLSX exports from Amazon Ads or downstream tools such as Seller Central, Advertising Console, Lingxing, ERP exports, BI exports, or manually combined spreadsheets.

Common useful columns:

| Concept | Common column names |
|---|---|
| Campaign | campaign, campaign name, ad campaign |
| Ad group | ad group, ad group name |
| Keyword/target | keyword, targeting, target |
| Search term | customer search term, search term, buyer search term |
| Match type | match type |
| Impressions | impressions |
| Clicks | clicks |
| Spend | spend, cost, ad spend |
| Sales | sales, 7 day total sales, 14 day total sales |
| Orders | orders, purchases, conversions |
| CPC | cpc, cost per click |
| ACOS | acos, advertising cost of sales |
| Bid | bid, keyword bid, default bid |
| Budget | budget, daily budget |

If key columns are missing, still summarize available metrics and label recommendations as `investigate` instead of inventing values.

## Decision Rules

Use these as defaults, then adjust for the user's category, margins, and growth goal.

| Action | Default trigger | Recommendation |
|---|---|---|
| Negative exact | Clicks >= 12, orders = 0, spend > 0 | Add exact negative for search term, unless branded/strategic |
| Bid down | Orders > 0 and ACOS > target ACOS * 1.3 | Reduce bid 10-25%; stronger cut when ACOS is very high |
| Bid down no-sale | Clicks >= 8 and orders = 0 | Reduce bid 15-30% if not ready for negative |
| Bid up | Orders >= 2 and ACOS < target ACOS * 0.7 | Increase bid 5-15% if budget and inventory allow |
| Harvest keyword | Search term orders >= 2 and ACOS <= target ACOS | Add as exact phrase/exact keyword or product target |
| Protect winner budget | Campaign ACOS <= target ACOS and budget usage appears constrained | Increase budget 10-30% |
| Reduce budget | High spend, poor ACOS, low conversions | Shift budget toward winners |

For launches, ranking pushes, branded defense, and high-LTV products, state that ACOS thresholds may be intentionally relaxed.

## Output Format

Return a concise answer plus a machine-reviewable table. Include:

- `priority`: high, medium, low
- `action`: negative_exact, bid_down, bid_up, harvest_keyword, harvest_asin, budget_up, budget_down, investigate
- `campaign`, `ad_group`, `keyword_or_target`, `search_term`
- `evidence`: clicks, spend, sales, orders, ACOS, CVR, CPC
- `recommendation`: exact operational action
- `reason`: short explanation
- `risk_note`: why a human should review before applying

When producing a spreadsheet, put the action table first, then summary tabs by campaign, target, and search term when data supports it.

## Script

Use `scripts/analyze_ads_report.py` for repeatable first-pass analysis. It:

- reads CSV and XLSX files,
- maps common English and Chinese Amazon Ads columns,
- computes CTR, CPC, CVR, ACOS, and ROAS where possible,
- writes an action-oriented recommendations CSV.

Run `python scripts/analyze_ads_report.py --help` for parameters.

The script is a starting point, not a final authority. Always review strategic exclusions such as brand terms, competitor conquesting, launch campaigns, low-stock products, and top-of-search ranking campaigns.

## Common Mistakes

- Do not negative a term only because it has high spend if it has attributed orders or strategic ranking value.
- Do not raise bids on winners when inventory is low, Buy Box is unstable, listing conversion is broken, or budget is intentionally capped.
- Do not compare ACOS across products with very different margins without noting the margin difference.
- Do not mix Sponsored Products, Sponsored Brands, and Sponsored Display without labeling report type and attribution window.
- Do not claim causal lift from an export alone; frame findings as optimization heuristics unless experiment data exists.

## References

Read `references/metric-definitions.md` when explaining metrics or when the user asks why a recommendation was made.
