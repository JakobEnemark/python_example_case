"""Tests for report generation."""

import pytest

from inventory.models import Product, Category
from inventory.store import InventoryStore
from inventory.reports import ReportGenerator


@pytest.fixture
def report_store() -> InventoryStore:
    store = InventoryStore()
    store.add_product(Product("R-1", "Expensive Item", 10, Category.ELECTRONICS, 500.0))
    store.add_product(Product("R-2", "Cheap Item", 200, Category.OTHER, 5.0))
    store.add_product(Product("R-3", "Mid Item", 30, Category.TOOLS, 100.0))
    return store


class TestReportGenerator:
    def test_summary(self, report_store):
        report = ReportGenerator(report_store)
        s = report.summary()
        assert s["total_products"] == 3
        assert s["total_value"] == 9000.0  # 5000 + 1000 + 3000
        assert s["low_stock_count"] == 0

    def test_category_breakdown(self, report_store):
        report = ReportGenerator(report_store)
        breakdown = report.category_breakdown()
        assert breakdown["electronics"] == 1
        assert breakdown["other"] == 1
        assert breakdown["tools"] == 1

    def test_top_value_products(self, report_store):
        report = ReportGenerator(report_store)
        top = report.top_value_products(2)
        assert len(top) == 2
        assert top[0]["sku"] == "R-1"  # 10 * 500 = 5000
        assert top[1]["sku"] == "R-3"  # 30 * 100 = 3000

    def test_format_text_report_contains_header(self, report_store):
        report = ReportGenerator(report_store)
        text = report.format_text_report()
        assert "INVENTORY REPORT" in text
        assert "9,000.00 DKK" in text
