# Amazon Ads Metric Definitions

Use these definitions when interpreting Amazon Ads reports.

| Metric | Formula | Notes |
|---|---|---|
| CTR | clicks / impressions | Low CTR can indicate weak main image, price, title, targeting, or relevance. |
| CPC | spend / clicks | Compare CPC against conversion rate and product margin, not in isolation. |
| CVR | orders / clicks | Low CVR often points to listing, price, review, coupon, Buy Box, inventory, or targeting mismatch. |
| ACOS | ad spend / attributed ad sales | Lower is not always better during launch, ranking, or defensive branded campaigns. |
| ROAS | attributed ad sales / ad spend | ROAS is the inverse of ACOS. |
| TACOS | ad spend / total sales | Requires total sales outside the ad report; do not compute unless total sales are provided. |

Default interpretation:

- High clicks and zero orders: consider negative keyword or bid reduction.
- Good orders and low ACOS: consider bid increase, budget increase, and exact-match harvesting.
- High ACOS with orders: reduce bid, inspect listing conversion, or move query into a lower-bid campaign.
- High spend with no sales at campaign level: investigate targeting quality, search term waste, and budget allocation.

Human review checklist before applying:

- Is the term branded, competitor, seasonal, or part of a ranking push?
- Is the product in stock and winning the Buy Box?
- Is the listing price, coupon, review count, rating, and image competitive?
- Is the campaign objective profit, launch, defense, clearance, or traffic learning?
- Are attribution windows consistent across compared reports?
