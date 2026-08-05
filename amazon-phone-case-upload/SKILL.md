---
name: amazon-phone-case-upload
description: Use when generating Amazon bulk upload spreadsheets for phone cases with iPhone model and color/size variations, especially for US marketplace flat files, parent-child SKU setups, GTIN exemption, or template filling.
---

# Amazon Phone Case Bulk Upload

Use this skill for Amazon Seller Central flat files for phone cases with `SizeName` or `ColorName-SizeName` variation themes.

## Use When

- User needs an Amazon bulk upload file for phone cases
- User has iPhone model variations
- User has both model and color variations
- User needs parent-child rows, GTIN exemption, or template export

## Core Rules

- Use the downloaded Amazon template copy only.
- Load the workbook in normal write mode, not `read_only=True`.
- Build the column map from template header row 3.
- Parent row is row 4; children start at row 5.
- For model-only listings, use `SizeName`.
- For model + color listings, use `ColorName-SizeName`.
- Child rows must fill both `size_name`/`size_map` and `color_name`/`color_map` when the template has those columns.
- Always set `parent_child`, `parent_sku`, `relationship_type`, and `variation_theme`.
- Fill `manufacturer` for parent and every child.
- Fill `external_product_id_type = GTIN Exemption` and leave `external_product_id` empty.
- Export the final upload file as tab-delimited `.txt` with CRLF line endings.

## Required Field Order

1. `feed_product_type`, `item_sku`, `brand_name`
2. `item_name`, `manufacturer`, `product_description`
3. `parent_child`, `parent_sku`, `relationship_type`, `variation_theme`
4. `size_name`, `size_map`, `color_name`, `color_map`
5. `bullet_point1`-`bullet_point5`, `generic_keywords`
6. `special_features1`
7. `form_factor`, `theme`, `pattern_name`, `material_type`
8. `included_components`, `compatible_phone_models1`
9. `external_product_id_type`
10. package dimensions and units
11. `list_price`, quantity, `condition_type`
12. `country_of_origin`

## Script

Use `fill_phone_case_template.py` in this folder for the default workflow. Adjust only the CONFIG section: brand, parent SKU, child SKU prefix, colors, models, title text, and output paths.

## Pitfalls

- `CELLULAR_PHONE_CASE` is wrong; use `cellularphonecase`
- Parent must have `item_name` and `manufacturer`
- Child `relationship_type` must be `Variation`
- Do not put a value in `merchant_shipping_group_name`
- Export to `.txt`; do not upload `.xlsm`
- Keep title length within 75 characters

