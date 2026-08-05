#!/usr/bin/env python3
"""
Amazon Phone Case Bulk Upload Template Filler
=============================================
Fills a downloaded Amazon flat file template (.xlsm) with phone case
variation data, then exports a .txt (tab-delimited) for upload.

Usage:
  1. Download template from Seller Central > Inventory > Add Products via Upload
  2. Set CONFIG below (brand, SKUs, iPhone models, listing content)
  3. Run: python fill_phone_case_template.py
  4. Upload the resulting .txt file to Seller Central
"""

import openpyxl
import os

# =========================================================================
# CONFIG — Customize these for each product
# =========================================================================

INPUT_TEMPLATE = r"D:\path\to\downloaded_template.xlsm"
OUTPUT_DIR = r"D:\path\to\output"

BRAND = "FXFOOT"
PARENT_SKU = "CAOMEI-DJ-P"
CHILD_SKU_PREFIX = "CMDJ"

PRODUCT_TYPE = "cellularphonecase"
VARIATION_THEME = "SizeName"  # Use "ColorName-SizeName" when COLORS has multiple entries.

# iPhone models: (SKU suffix, size_name, compatible_model)
# size_name is what appears in the size dropdown on product page
MODELS = [
    ("IP11", "iPhone 11", "iPhone 11"),
    ("IP11PRO", "iPhone 11 Pro", "iPhone 11 Pro"),
    ("IP11PROMAX", "iPhone 11 Pro Max", "iPhone 11 Pro Max"),
    ("IP12", "iPhone 12", "iPhone 12"),
    ("IP12MINI", "iPhone 12 mini", "iPhone 12 mini"),
    ("IP12PRO", "iPhone 12 Pro", "iPhone 12 Pro"),
    ("IP12PROMAX", "iPhone 12 Pro Max", "iPhone 12 Pro Max"),
    ("IP13", "iPhone 13", "iPhone 13"),
    ("IP13MINI", "iPhone 13 mini", "iPhone 13 mini"),
    ("IP13PRO", "iPhone 13 Pro", "iPhone 13 Pro"),
    ("IP13PROMAX", "iPhone 13 Pro Max", "iPhone 13 Pro Max"),
    ("IP14", "iPhone 14", "iPhone 14"),
    ("IP14PLUS", "iPhone 14 Plus", "iPhone 14 Plus"),
    ("IP14PRO", "iPhone 14 Pro", "iPhone 14 Pro"),
    ("IP14PROMAX", "iPhone 14 Pro Max", "iPhone 14 Pro Max"),
    ("IP15", "iPhone 15", "iPhone 15"),
    ("IP15PLUS", "iPhone 15 Plus", "iPhone 15 Plus"),
    ("IP15PRO", "iPhone 15 Pro", "iPhone 15 Pro"),
    ("IP15PROMAX", "iPhone 15 Pro Max", "iPhone 15 Pro Max"),
    ("IP16", "iPhone 16", "iPhone 16"),
    ("IP16PLUS", "iPhone 16 Plus", "iPhone 16 Plus"),
    ("IP16PRO", "iPhone 16 Pro", "iPhone 16 Pro"),
    ("IP16PROMAX", "iPhone 16 Pro Max", "iPhone 16 Pro Max"),
    ("IP17", "iPhone 17", "iPhone 17"),
    ("IP17PRO", "iPhone 17 Pro", "iPhone 17 Pro"),
    ("IP17PROMAX", "iPhone 17 Pro Max", "iPhone 17 Pro Max"),
]

# Colors: (display name, color_map, sku_suffix, title_word)
COLORS = [
    ("Clear", "Clear", "CLR", ""),
]

# =========================================================================
# LISTING CONTENT — Per 2026 July regulations
# =========================================================================

def make_title(size_name: str, color_word: str = "", design_name: str = "3D Strawberry") -> str:
    """
    Generate title ≤75 chars per 2026 July regulation.
    Formula: [Brand] [Design] Phone Case for [Size] [Material] [Style]
    """
    color_part = f" {color_word}" if color_word else ""
    base = f"{BRAND} {design_name} Phone Case for {size_name}{color_part} Cute Soft TPU Clear"
    if len(base) <= 75:
        return base
    # Fallback: shorten
    return f"{BRAND} {design_name} Case for {size_name}{color_part} Cute Soft Clear TPU"

PARENT_TITLE = f"{BRAND} 3D Strawberry Phone Case Cute Soft TPU Clear Bumper"

BULLET1 = "3D resin strawberry with bows and stars. Cute and vibrant; clear back shows your iPhone's color with playful personality."
BULLET2 = "Soft TPU absorbs shock, resists yellowing. Slim, flexible, and lightweight; reinforced corners protect against daily drops."
BULLET3 = "Raised camera bezel and red ring guard lenses against scratches. Elevated edges protect the screen when placed face-down."
BULLET4 = "Precise cutouts for camera, buttons, and ports. Wireless charging and Face ID fully supported; slim fit adds no bulk."
BULLET5 = "A great gift for teen girls, women, strawberry lovers. Bright colors stay vibrant; fits easily into pockets and small bags."

DESCRIPTION = (
    "Show off your sweet style with the FXFOOT 3D Strawberry Phone Case. "
    "Featuring adorable 3D resin strawberries, delicate bows, and twinkling stars, "
    "this case brings a playful and vibrant look to your iPhone. "
    "The crystal-clear back panel lets your phone's original color shine through while showing off the charming design.\n\n"
    "Made from soft, flexible TPU that absorbs shock and resists yellowing over time. "
    "Reinforced corners provide reliable drop protection, while the slim profile keeps your phone lightweight and easy to carry. "
    "The raised camera bezel safeguards your lenses, and elevated screen edges protect against scratches when placed face-down.\n\n"
    "Precision cutouts ensure easy access to buttons, ports, and cameras. "
    "Fully compatible with wireless charging and Face ID — no need to remove the case. "
    "The perfect gift for strawberry lovers, teens, and anyone who wants a cute yet protective phone case."
)

SEARCH_TERMS = (
    "strawberry fruit bow star pink red silicone rubber gel slim thin "
    "shockproof cover skin shell women gift "
    "15promax 14promax 13promax 12promax 11promax plus mini "
    "transparent bling resin quicksand camera lens charger wireless"
)

# Package info
PACKAGE_HEIGHT = 1.5  # cm
PACKAGE_LENGTH = 12.0  # cm
PACKAGE_WIDTH = 8.0  # cm
PACKAGE_WEIGHT = 60  # grams

PRICE = 19.9
QUANTITY = 0

COLOR_NAME = "Clear"
MATERIAL = "Thermoplastic Polyurethane"
DESIGN_THEME = "Floral"
PATTERN = "Floral"
FORM_FACTOR = "Basic Case"
INCLUDED_COMPONENTS = "Card Holder"

# =========================================================================
# PRECHECK
# =========================================================================

def precheck():
    """Validate listing content before filling template."""
    errors = []
    for _, size_name, _, color_word in [(m[0], m[1], m[2], c[3]) for c in COLORS for m in MODELS]:
        title = make_title(size_name, color_word)
        if len(title) > 75:
            errors.append(f"Title too long for {size_name}/{color_word or 'NoColor'}: {len(title)} chars")
    for i, bp in enumerate([BULLET1, BULLET2, BULLET3, BULLET4, BULLET5], 1):
        if len(bp) > 125:
            errors.append(f"Bullet {i} too long: {len(bp)} chars")
    st_bytes = len(SEARCH_TERMS.encode("utf-8"))
    if st_bytes > 250:
        errors.append(f"Search terms over 250 bytes: {st_bytes}")
    if len(PARENT_TITLE) > 75:
        errors.append(f"Parent title too long: {len(PARENT_TITLE)} chars")

    if errors:
        print("PRECHECK FAILED:")
        for e in errors:
            print(f"  ERROR: {e}")
        return False

    print("Precheck passed:")
    max_title = max(len(make_title(size_name, color_word)) for _, size_name, _, color_word in [(m[0], m[1], m[2], c[3]) for c in COLORS for m in MODELS])
    print(f"  Max title: {max_title} chars (limit 75)")
    for i, bp in enumerate([BULLET1, BULLET2, BULLET3, BULLET4, BULLET5], 1):
        print(f"  Bullet {i}: {len(bp)} chars (limit 125)")
    print(f"  Search Terms: {st_bytes} bytes (limit 250)")
    return True

# =========================================================================
# MAIN
# =========================================================================

def fill_template():
    if not precheck():
        print("\nAborting. Fix errors above first.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load template (NOT read_only mode!)
    print(f"\nLoading: {INPUT_TEMPLATE}")
    wb = openpyxl.load_workbook(INPUT_TEMPLATE, keep_vba=True)
    ws = wb["Template"]

    # Build column map from row 3
    COL = {}
    for c in range(1, ws.max_column + 1):
        v = ws.cell(row=3, column=c).value
        if v:
            COL[str(v).strip()] = c

    print(f"Template: {ws.max_row} rows, {ws.max_column} cols, {len(COL)} mapped fields")

    # Clear old data rows
    for r in range(4, ws.max_row + 1):
        for c in range(1, ws.max_column + 1):
            ws.cell(row=r, column=c).value = None

    # ---- Parent (row 4) ----
    r = 4
    ws.cell(row=r, column=COL["feed_product_type"]).value = PRODUCT_TYPE
    ws.cell(row=r, column=COL["item_sku"]).value = PARENT_SKU
    ws.cell(row=r, column=COL["brand_name"]).value = BRAND
    ws.cell(row=r, column=COL["parent_child"]).value = "Parent"
    ws.cell(row=r, column=COL["variation_theme"]).value = VARIATION_THEME
    ws.cell(row=r, column=COL["item_name"]).value = PARENT_TITLE
    ws.cell(row=r, column=COL["manufacturer"]).value = BRAND

    # ---- Children ----
    row = 5
    for color_name, color_map, color_suffix, color_word in COLORS:
        for sku_suffix, size_name, model_name in MODELS:
            r = row
            row += 1
            sku = f"{CHILD_SKU_PREFIX}-{color_suffix}-{sku_suffix}" if len(COLORS) > 1 else f"{CHILD_SKU_PREFIX}-{sku_suffix}"
            title = make_title(size_name, color_word)

            # Core
            ws.cell(row=r, column=COL["feed_product_type"]).value = PRODUCT_TYPE
            ws.cell(row=r, column=COL["item_sku"]).value = sku
            ws.cell(row=r, column=COL["brand_name"]).value = BRAND
            ws.cell(row=r, column=COL["update_delete"]).value = "Update"

            # Title & Description
            ws.cell(row=r, column=COL["item_name"]).value = title
            ws.cell(row=r, column=COL["manufacturer"]).value = BRAND
            ws.cell(row=r, column=COL["product_description"]).value = DESCRIPTION

            # GTIN Exemption
            ws.cell(row=r, column=COL["external_product_id_type"]).value = "GTIN Exemption"

            # Variation
            ws.cell(row=r, column=COL["parent_child"]).value = "Child"
            ws.cell(row=r, column=COL["parent_sku"]).value = PARENT_SKU
            ws.cell(row=r, column=COL["relationship_type"]).value = "Variation"
            ws.cell(row=r, column=COL["variation_theme"]).value = VARIATION_THEME

            # Bullet Points
            ws.cell(row=r, column=COL["bullet_point1"]).value = BULLET1
            ws.cell(row=r, column=COL["bullet_point2"]).value = BULLET2
            ws.cell(row=r, column=COL["bullet_point3"]).value = BULLET3
            ws.cell(row=r, column=COL["bullet_point4"]).value = BULLET4
            ws.cell(row=r, column=COL["bullet_point5"]).value = BULLET5

            # Search Terms
            ws.cell(row=r, column=COL["generic_keywords"]).value = SEARCH_TERMS

            # Special Features (required!)
            ws.cell(row=r, column=COL["special_features1"]).value = "Wireless"

            # Size & Color
            ws.cell(row=r, column=COL["size_name"]).value = size_name
            ws.cell(row=r, column=COL["size_map"]).value = size_name
            ws.cell(row=r, column=COL["color_name"]).value = color_name
            if "color_map" in COL:
                ws.cell(row=r, column=COL["color_map"]).value = color_map

            # Material
            ws.cell(row=r, column=COL["material_type"]).value = MATERIAL

            # Design attributes (all required)
            ws.cell(row=r, column=COL["pattern_name"]).value = PATTERN
            ws.cell(row=r, column=COL["theme"]).value = DESIGN_THEME
            ws.cell(row=r, column=COL["form_factor"]).value = FORM_FACTOR
            ws.cell(row=r, column=COL["included_components"]).value = INCLUDED_COMPONENTS

            # Compatibility
            ws.cell(row=r, column=COL["compatible_phone_models1"]).value = model_name

            # Package dimensions
            ws.cell(row=r, column=COL["package_height"]).value = PACKAGE_HEIGHT
            ws.cell(row=r, column=COL["package_length"]).value = PACKAGE_LENGTH
            ws.cell(row=r, column=COL["package_width"]).value = PACKAGE_WIDTH
            ws.cell(row=r, column=COL["package_weight"]).value = PACKAGE_WEIGHT
            ws.cell(row=r, column=COL["package_height_unit_of_measure"]).value = "CM"
            ws.cell(row=r, column=COL["package_length_unit_of_measure"]).value = "CM"
            ws.cell(row=r, column=COL["package_width_unit_of_measure"]).value = "CM"
            ws.cell(row=r, column=COL["package_weight_unit_of_measure"]).value = "GR"

            # Country
            ws.cell(row=r, column=COL["country_of_origin"]).value = "CN"

            # Price & Quantity
            ws.cell(row=r, column=COL["fulfillment_availability#1.quantity"]).value = QUANTITY
            ws.cell(row=r, column=COL["purchasable_offer[marketplace_id=ATVPDKIKX0DER]#1.our_price#1.schedule#1.value_with_tax"]).value = PRICE
            ws.cell(row=r, column=COL["list_price"]).value = PRICE

            # Condition
            ws.cell(row=r, column=COL["condition_type"]).value = "New"

    print(f"Filled: 1 parent + {len(MODELS) * len(COLORS)} children")

    # ---- Save .xlsm (for record) ----
    xlsm_path = os.path.join(OUTPUT_DIR, f"phone_case_{BRAND}_{PARENT_SKU}.xlsm")
    wb.save(xlsm_path)
    print(f"Saved: {xlsm_path}")

    # ---- Export .txt (tab-delimited, CRLF) ----
    txt_path = os.path.join(OUTPUT_DIR, f"phone_case_{BRAND}_{PARENT_SKU}.txt")

    lines = []
    for r in range(1, ws.max_row + 1):
        cells = []
        for c in range(1, ws.max_column + 1):
            v = ws.cell(row=r, column=c).value
            if v is None:
                cells.append('')
            else:
                s = str(v).replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
                cells.append(s)
        lines.append('\t'.join(cells))

    with open(txt_path, 'w', encoding='utf-8', newline='') as f:
        for line in lines:
            f.write(line + '\r\n')

    print(f"Upload file: {txt_path}")
    print(f"Size: {os.path.getsize(txt_path):,} bytes")

    wb.close()

    # ---- Quick Verify ----
    print("\n=== VERIFICATION ===")
    wb2 = openpyxl.load_workbook(xlsm_path)
    ws2 = wb2["Template"]
    COL2 = {}
    for c in range(1, ws2.max_column + 1):
        v = ws2.cell(row=3, column=c).value
        if v:
            COL2[str(v).strip()] = c

    errors = []
    # Check parent
    if ws2.cell(row=4, column=COL2["item_name"]).value is None:
        errors.append("Parent: item_name MISSING")
    if ws2.cell(row=4, column=COL2["manufacturer"]).value is None:
        errors.append("Parent: manufacturer MISSING")

    # Check children
    row = 5
    for color_name, color_map, color_suffix, color_word in COLORS:
        for sku_suffix, size_name, model_name in MODELS:
            r = row
            row += 1
            sku = f"{CHILD_SKU_PREFIX}-{color_suffix}-{sku_suffix}" if len(COLORS) > 1 else f"{CHILD_SKU_PREFIX}-{sku_suffix}"

            title = ws2.cell(row=r, column=COL2["item_name"]).value or ""
            manufacturer = ws2.cell(row=r, column=COL2["manufacturer"]).value or ""
            pt = ws2.cell(row=r, column=COL2["feed_product_type"]).value or ""
            pc = ws2.cell(row=r, column=COL2["parent_child"]).value or ""
            rel = ws2.cell(row=r, column=COL2["relationship_type"]).value or ""
            sf1 = ws2.cell(row=r, column=COL2["special_features1"]).value or ""
            pidt = ws2.cell(row=r, column=COL2["external_product_id_type"]).value or ""

            if len(str(title)) > 75:
                errors.append(f"{sku}: Title {len(str(title))} chars")
            if not manufacturer:
                errors.append(f"{sku}: manufacturer MISSING!")
            if pt != PRODUCT_TYPE:
                errors.append(f"{sku}: ProductType={pt}")
            if pc != "Child":
                errors.append(f"{sku}: Parentage={pc}")
            if rel != "Variation":
                errors.append(f"{sku}: RelationshipType={rel}")
            if not sf1:
                errors.append(f"{sku}: special_features1 MISSING!")
            if pidt != "GTIN Exemption":
                errors.append(f"{sku}: PIDType={pidt}")

    wb2.close()

    if errors:
        print(f"\n{len(errors)} ERRORS:")
        for e in errors:
            print(f"  ERROR: {e}")
    else:
        print("\nALL VERIFICATIONS PASSED!")

    print(f"\nUpload file ready: {txt_path}")

# =========================================================================
if __name__ == "__main__":
    fill_template()
