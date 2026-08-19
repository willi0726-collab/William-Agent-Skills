---
name: amazon-phone-case-upload
description: Use when generating or repairing Amazon phone-case bulk upload spreadsheets and processing summaries, especially for US flat files, parent-child variations, GTIN exemption, invalid dropdown values, missing required fields, or unit-format errors.
---

# Amazon Phone Case Bulk Upload

Use this skill for Amazon Seller Central phone-case flat files. Use the fixed workspace template as the default schema and still read its dynamic row settings.

## Use When

- User needs an Amazon bulk upload file for phone cases
- User has iPhone model variations
- User has both model and color variations
- User needs parent-child rows, GTIN exemption, or template export

## Core Rules

- Default to the fixed template at `C:\Users\ZhuanZ\Documents\领星自动化\templates\amazon-phone-case-upload\CELLULAR_PHONE_CASE.xlsm`.
- Do not select a template from store folders, processing summaries, or prior outputs. Replace the fixed template only when the user explicitly provides a newer template and asks to make it the new default.
- Load the workbook in normal write mode, not `read_only=True`.
- Read `labelRow`, `attributeRow`, and `dataRow` from the template `settings=` string. Fall back to legacy rows 2/3/4 only when settings are absent.
- Map fields by the underlying attribute names in `attributeRow`; never rely on Excel column letters or duplicate display labels.
- Choose a variation theme from the current template's Dropdown Lists. In the 2026 US cellular-phone-case template, color + model uses `COLOR/COMPATIBLE_PHONE_MODELS`.
- Under `COLOR/COMPATIBLE_PHONE_MODELS`, every child must have a unique `(color, compatible phone model)` coordinate. If two physically different styles share a base color, use concise evidence-backed style qualifiers in the customer-facing color value and title; do not submit both as the same `Brown + model` combination.
- Child rows must fill both `size_name`/`size_map` and `color_name`/`color_map` when the template has those columns.
- Always set `parent_child`, `parent_sku`, `relationship_type`, and `variation_theme`.
- Fill `manufacturer` for parent and every child.
- For a GTIN-exempt account, use the current template's valid Product Id Type value. For this workflow the confirmed value is `GTIN Exempt`; leave Product Id blank.
- Fill `Number of Items = 1`, `Part Number = SKU`, and set Compatible Devices to the exact phone model when those fields exist.
- Analyze supplied product evidence to fill supported attributes such as Finish Type, Style, Pattern, Theme, material, included components, and special features. Never infer unsupported certifications or performance ratings.
- Use exact dropdown units from the current template. For this workflow, dimensional units are `Centimeters` and package weight is `Grams`; do not substitute legacy abbreviations such as `CM` or `GR`.
- Use the fixed template's dropdown display value `China` for Country of Origin; do not use the code `CN`.
- Before delivery, compare every populated cell that has a `Valid Values` entry against that template row and reject any non-matching display value.
- When provided, fill both decimal and string thickness fields plus the thickness unit, warranty description, and battery-required status.
- Distinguish the two Item Length fields. In this template, standalone `item_length` accepts only `Inches`, so convert centimeters with `inches = centimeters / 2.54`; the Item Dimensions length/width/height group can remain in `Centimeters`.
- Populate parent-level required fields too: Product Description, at least Bullet Point #1, Country of Origin, and Are batteries required.
- Fill Item Highlight (`title_differentiation...`) when present; keep it evidence-backed and within 125 characters.
- Keep Item Name within 75 characters and backend Generic Keyword within 250 UTF-8 bytes.
- Offer fields must follow the user's latest instruction. For FBM, use the template's exact fulfillment value, quantity, price, and shipping template. Leave `Skip Offer` blank when an offer is supplied.
- Use only the current template's exact dropdown display values. In this template, full replacement is `Create or Replace (Full Update)`, not `Full Update`.
- Preserve VBA with `keep_vba=True` and save the filled `.xlsm` copy before exporting.
- Generate only the preserved `.xlsm` by default. Export tab-delimited CRLF `.txt` only when the user explicitly requests TXT.

## Product Profile Cache

Use `product_profile_cache.py` and store one UTF-8 JSON profile per parent/style under `C:\Users\ZhuanZ\Documents\领星自动化\product_profiles\amazon-phone-case-upload`. The profile is the reusable source for product facts, listing copy, model rules, and image mappings; it is not the final upload file.

At the start of each run:

1. Load an existing profile before reading images or regenerating listing copy.
2. Compute a content hash for each supplied image or ZIP entry.
3. When the hash matches a cached asset whose `verified` flag is true, reuse the verified Cloudinary URL and cached image role. A cached Hero role remains the main image.
4. Compare requested facts, template identity, model scope, and source hashes with the profile. Analyze only changed or new evidence; reuse unchanged titles, highlights, bullets, descriptions, search terms, and attributes.
5. Generate repeated model rows deterministically from the style-level content. Do not ask the model to rewrite identical copy for every child SKU.
6. After public URL readback and workbook validation pass, atomically save the updated profile. Do not cache failed uploads or unverified URLs.

XLSM remains the default deliverable. The cache reduces repeated analysis and upload work; switching to TXT is not an optimization strategy.

Minimum profile shape:

```json
{
  "schema_version": 1,
  "product": {"brand": "FXFOOT", "parent_sku": "PARENT", "style_code": "STYLE"},
  "content": {"title_pattern": "...", "bullets": ["..."], "search_terms": "..."},
  "assets": {"Hero.jpg": {"sha256": "...", "url": "https://...", "verified": true, "role": "main"}}
}
```

## Processing Summary Repair

When Amazon returns a `processing-summary.xlsm`:

1. Read `Feed Processing Summary` and group errors by code, field, and SKU.
2. Treat the detailed error as the root cause; generic `90041` is often only the row-level failure wrapper.
3. Read valid values from that same workbook's `Valid Values` or `Dropdown Lists` sheet.
4. Preserve its dynamic `dataRow`; processing summaries commonly start at row 7 and add three feedback columns.
5. Clear feedback status/error cells before resubmission and retain the template structure and VBA.
6. Revalidate every affected row, not only the first SKU.
7. For `100730` with near-identical items, compare variation coordinates, titles, and product details across the affected SKUs. A later `13013` can be a downstream offer-attachment failure while the catalog record is still processing; fix the product identity collision first, then resubmit the corrected workbook once.

### Confirmed mappings from real feedback

| Error | Wrong value | Correct handling |
|---|---|---|
| `90057` Listing Action | `Full Update` | `Create or Replace (Full Update)` |
| `90244` standalone Item Length Unit | `Centimeters` | convert cm to inches, unit `Inches` |
| `90220` parent required fields | blank parent detail fields | fill description, Bullet #1, country, batteries required |
| `100730` duplicate product details | distinct designs share the same color + compatible model coordinate and near-identical titles | assign evidence-backed style-qualified color/title values so every child coordinate is unique |
| `13013` offer cannot be added | catalog product is not ready, often downstream of product processing | resolve the product-level issue first, then resubmit the corrected row with its FBM offer |

Keep the separate Item Dimensions group in centimeters. Example: 12 cm standalone Item Length becomes `4.72 Inches`, while Item Dimensions can remain `12 × 5 × 1 Centimeters`.

## Required Field Order

1. SKU, Product Type, Brand Name, Listing Action
2. `item_name`, `manufacturer`, `product_description`
3. `parent_child`, `parent_sku`, `relationship_type`, `variation_theme`
4. `size_name`, `size_map`, `color_name`, `color_map`
5. `bullet_point1`-`bullet_point5`, `generic_keywords`
6. `special_features1`
7. `form_factor`, `theme`, `pattern_name`, `material_type`
8. `included_components`, `compatible_phone_models1`
9. Product Id fields only when applicable
10. package dimensions and units
11. offer/fulfillment fields or `Skip Offer`, plus `condition_type`
12. `country_of_origin`

## Script

Use `fill_phone_case_template.py` for the fixed-template workflow and `product_profile_cache.py` for incremental reuse. Adjust the CONFIG section and listing content, then run the tests before producing customer files.

## Pitfalls

- Product Type values differ by template generation (`cellularphonecase` in legacy files, `CELLULAR_PHONE_CASE` in the current attribute schema); follow the current template.
- Parent must have `item_name` and `manufacturer`
- Child `relationship_type` must be `Variation`
- Do not reuse legacy themes such as `SizeName-ColorName` unless they appear in the current template's allowed values.
- Do not invent compatibility, protection ratings, charging support, or materials not supported by supplied evidence.
- For the confirmed FXFOOT crossbody wallet series, read `references/fxfoot-crossbody-series.md` before mapping AXKB-ZS or XKAXKB-Z images and claims.
- Deliver both the preserved `.xlsm` and CRLF `.txt` when the user requests both.
