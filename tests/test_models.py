"""Tests for the inventory models."""

import pytest
from datetime import datetime

from inventory.models import Product, Category


class TestCategory:
    def test_from_string_valid(self):
        assert Category.from_string("electronics") == Category.ELECTRONICS
        assert Category.from_string("FOOD") == Category.FOOD
        assert Category.from_string(" Tools ") == Category.TOOLS

    def test_from_string_unknown_returns_other(self):
        assert Category.from_string("widgets") == Category.OTHER
        assert Category.from_string("") == Category.OTHER


class TestProduct:
    def make_product(self, **overrides) -> Product:
        defaults = {
            "sku": "TEST-001",
            "name": "Test Product",
            "quantity": 50,
            "category": Category.ELECTRONICS,
            "price": 99.95,
        }
        defaults.update(overrides)
        return Product(**defaults)

    def test_creation(self):
        p = self.make_product()
        assert p.sku == "TEST-001"
        assert p.quantity == 50
        assert isinstance(p.last_updated, datetime)

    def test_negative_quantity_raises(self):
        with pytest.raises(ValueError, match="negative"):
            self.make_product(quantity=-1)

    def test_negative_price_raises(self):
        with pytest.raises(ValueError, match="negative"):
            self.make_product(price=-10)

    def test_empty_sku_raises(self):
        with pytest.raises(ValueError, match="SKU"):
            self.make_product(sku="")

    def test_total_value(self):
        p = self.make_product(quantity=10, price=25.0)
        assert p.total_value == 250.0

    def test_is_low_stock(self):
        assert self.make_product(quantity=5).is_low_stock is True
        assert self.make_product(quantity=10).is_low_stock is False
        assert self.make_product(quantity=100).is_low_stock is False

    def test_adjust_stock_add(self):
        p = self.make_product(quantity=10)
        p.adjust_stock(5)
        assert p.quantity == 15

    def test_adjust_stock_remove(self):
        p = self.make_product(quantity=10)
        p.adjust_stock(-3)
        assert p.quantity == 7

    def test_adjust_stock_below_zero_raises(self):
        p = self.make_product(quantity=5)
        with pytest.raises(ValueError, match="Cannot remove"):
            p.adjust_stock(-10)

    def test_roundtrip_dict(self):
        p = self.make_product()
        data = p.to_dict()
        restored = Product.from_dict(data)
        assert restored.sku == p.sku
        assert restored.name == p.name
        assert restored.quantity == p.quantity
        assert restored.category == p.category
        assert restored.price == p.price
