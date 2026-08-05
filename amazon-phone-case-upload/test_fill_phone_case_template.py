import importlib.util
import tempfile
import unittest
from pathlib import Path

import openpyxl


SKILL_DIR = Path(__file__).parent
SCRIPT = SKILL_DIR / "fill_phone_case_template.py"
REQUIRED_HEADERS = [
    "feed_product_type", "item_sku", "brand_name", "parent_child",
    "variation_theme", "item_name", "manufacturer", "update_delete",
    "product_description", "external_product_id_type", "parent_sku",
    "relationship_type", "bullet_point1", "bullet_point2", "bullet_point3",
    "bullet_point4", "bullet_point5", "generic_keywords", "special_features1",
    "size_name", "size_map", "color_name", "color_map", "material_type",
    "pattern_name", "theme", "form_factor", "included_components",
    "compatible_phone_models1", "package_height", "package_length",
    "package_width", "package_weight", "package_height_unit_of_measure",
    "package_length_unit_of_measure", "package_width_unit_of_measure",
    "package_weight_unit_of_measure", "country_of_origin",
    "fulfillment_availability#1.quantity",
    "purchasable_offer[marketplace_id=ATVPDKIKX0DER]#1.our_price#1.schedule#1.value_with_tax",
    "list_price", "condition_type",
]


class FillTemplateTest(unittest.TestCase):
    def test_every_color_model_child_gets_commercial_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            template = tmp / "template.xlsm"
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Template"
            for column, header in enumerate(REQUIRED_HEADERS, 1):
                ws.cell(3, column, header)
            wb.save(template)

            spec = importlib.util.spec_from_file_location("phone_case_fill", SCRIPT)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.INPUT_TEMPLATE = str(template)
            module.OUTPUT_DIR = str(tmp / "output")
            module.MODELS = [("IP16", "iPhone 16", "iPhone 16"), ("IP17", "iPhone 17", "iPhone 17")]
            module.COLORS = [("Pink", "Pink", "PINK", "Pink"), ("Blue", "Blue", "BLUE", "Blue")]
            module.VARIATION_THEME = "ColorName-SizeName"
            module.fill_template()

            output = Path(module.OUTPUT_DIR) / f"phone_case_{module.BRAND}_{module.PARENT_SKU}.xlsm"
            result = openpyxl.load_workbook(output, data_only=False)
            sheet = result["Template"]
            columns = {sheet.cell(3, c).value: c for c in range(1, sheet.max_column + 1)}
            for row in range(5, 9):
                self.assertEqual(module.PRICE, sheet.cell(row, columns["list_price"]).value)
                self.assertEqual("CN", sheet.cell(row, columns["country_of_origin"]).value)
                self.assertEqual("New", sheet.cell(row, columns["condition_type"]).value)
                self.assertEqual(module.VARIATION_THEME, sheet.cell(row, columns["variation_theme"]).value)
            result.close()


if __name__ == "__main__":
    unittest.main()
