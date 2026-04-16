"""Tests for candidate tasks — DO NOT MODIFY this file."""

import pytest

from inventory.models import Product, Category
from inventory.store import InventoryStore
from inventory.reports import ReportGenerator


@pytest.fixture
def task_store() -> InventoryStore:
    store = InventoryStore()
    store.add_product(Product("T-1", "Well Stocked", 100, Category.TOOLS, 10.0))
    store.add_product(Product("T-2", "Low Item A", 3, Category.ELECTRONICS, 50.0))
    store.add_product(Product("T-3", "Low Item B", 7, Category.CLOTHING, 25.0))
    store.add_product(Product("T-4", "Borderline", 10, Category.FOOD, 15.0))
    return store


# ── Task 1: restock ─────────────────────────────────────────────

class TestRestock:
    def test_restocks_low_stock_only(self, task_store):
        restocked = task_store.restock(50)
        assert sorted(restocked) == ["T-2", "T-3"]

    def test_sets_target_quantity(self, task_store):
        task_store.restock(40)
        assert task_store.get_product("T-2").quantity == 40
        assert task_store.get_product("T-3").quantity == 40

    def test_does_not_change_sufficient_stock(self, task_store):
        task_store.restock(50)
        assert task_store.get_product("T-1").quantity == 100
        assert task_store.get_product("T-4").quantity == 10

    def test_returns_empty_when_all_stocked(self):
        store = InventoryStore()
        store.add_product(Product("OK-1", "Fine", 50, Category.OTHER, 5.0))
        assert store.restock() == []

    def test_default_target_is_50(self, task_store):
        task_store.restock()
        assert task_store.get_product("T-2").quantity == 50


# ── Task 2: low_stock_report ────────────────────────────────────

class TestLowStockReport:
    def test_contains_low_stock_products(self, task_store):
        report = ReportGenerator(task_store)
        text = report.low_stock_report()
        assert "LOW STOCK ALERT" in text
        assert "T-2" in text
        assert "T-3" in text
        assert "Low Item A" in text

    def test_does_not_include_sufficient_stock(self, task_store):
        report = ReportGenerator(task_store)
        text = report.low_stock_report()
        assert "T-1" not in text
        assert "T-4" not in text

    def test_shows_count(self, task_store):
        report = ReportGenerator(task_store)
        text = report.low_stock_report()
        assert "2 products need restocking" in text

    def test_all_stocked_message(self):
        store = InventoryStore()
        store.add_product(Product("OK-1", "Fine", 50, Category.OTHER, 5.0))
        report = ReportGenerator(store)
        text = report.low_stock_report()
        assert "sufficiently stocked" in text
