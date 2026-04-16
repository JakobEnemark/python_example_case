"""Tests for the inventory store."""

import pytest
from pathlib import Path

from inventory.models import Product, Category
from inventory.store import InventoryStore


@pytest.fixture
def store() -> InventoryStore:
    """An empty store."""
    return InventoryStore()


@pytest.fixture
def populated_store(store: InventoryStore) -> InventoryStore:
    """A store with a few products."""
    store.add_product(Product("A-001", "Widget", 100, Category.TOOLS, 25.0))
    store.add_product(Product("A-002", "Gadget", 5, Category.ELECTRONICS, 199.0))
    store.add_product(Product("A-003", "Widget Pro", 50, Category.TOOLS, 45.0))
    return store


class TestInventoryStore:
    def test_add_and_get(self, store):
        p = Product("X-1", "Item", 10, Category.OTHER, 5.0)
        store.add_product(p)
        assert store.get_product("X-1") is p

    def test_add_duplicate_raises(self, store):
        p = Product("X-1", "Item", 10, Category.OTHER, 5.0)
        store.add_product(p)
        with pytest.raises(KeyError, match="already exists"):
            store.add_product(Product("X-1", "Other", 1, Category.OTHER, 1.0))

    def test_remove_product(self, populated_store):
        removed = populated_store.remove_product("A-002")
        assert removed.name == "Gadget"
        assert "A-002" not in populated_store

    def test_remove_missing_raises(self, store):
        with pytest.raises(KeyError):
            store.remove_product("NOPE")

    def test_len_and_contains(self, populated_store):
        assert len(populated_store) == 3
        assert "A-001" in populated_store
        assert "Z-999" not in populated_store

    def test_search(self, populated_store):
        results = populated_store.search("widget")
        assert len(results) == 2
        assert all("Widget" in p.name for p in results)

    def test_search_no_match(self, populated_store):
        assert populated_store.search("nonexistent") == []

    def test_filter_by_category(self, populated_store):
        tools = populated_store.filter_by_category(Category.TOOLS)
        assert len(tools) == 2

    def test_low_stock(self, populated_store):
        low = populated_store.low_stock_products()
        assert len(low) == 1
        assert low[0].sku == "A-002"

    def test_total_inventory_value(self, populated_store):
        # 100*25 + 5*199 + 50*45 = 2500 + 995 + 2250 = 5745
        assert populated_store.total_inventory_value() == 5745.0

    def test_update_stock(self, populated_store):
        populated_store.update_stock("A-001", -10)
        assert populated_store.get_product("A-001").quantity == 90


class TestCSVPersistence:
    def test_save_and_load(self, populated_store, tmp_path):
        csv_path = tmp_path / "test.csv"
        written = populated_store.save_csv(csv_path)
        assert written == 3

        new_store = InventoryStore()
        loaded = new_store.load_csv(csv_path)
        assert loaded == 3
        assert new_store.get_product("A-001").name == "Widget"

    def test_load_skips_invalid_rows(self, tmp_path):
        csv_path = tmp_path / "bad.csv"
        csv_path.write_text(
            "sku,name,quantity,category,price,last_updated\n"
            "OK-1,Good Item,10,tools,25.0,2026-01-01T00:00:00\n"
            ",Bad Item,-5,tool,abc,2026-01-01T00:00:00\n",
            encoding="utf-8",
        )
        store = InventoryStore()
        loaded = store.load_csv(csv_path)
        assert loaded == 1
