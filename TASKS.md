# Coding Tasks

Complete both tasks below. The existing tests should continue to pass, and your new code should be covered by the tests provided in `tests/test_tasks.py`.

Run all tests with:
```bash
python -m pytest tests/ -v
```

---

## Task 1: Add a `restock` method to `InventoryStore`

In `inventory/store.py`, add a method called `restock` that automatically restocks **all** low-stock products to a given target quantity.

### Specification

```python
def restock(self, target: int = 50) -> list[str]:
    """Restock all low-stock products to the target quantity.

    Only products where quantity < 10 are restocked.
    Returns a list of SKUs that were restocked.
    """
```

- Only restock products that are currently below the low-stock threshold (quantity < 10)
- Set their quantity to exactly `target`
- Return a list of the SKUs that were restocked
- Update `last_updated` for each restocked product

### Example

If product `"A-002"` has quantity 5 and target is 50, after calling `restock(50)` it should have quantity 50.

---

## Task 2: Add a `low_stock_report` method to `ReportGenerator`

In `inventory/reports.py`, add a method that returns a formatted string listing all low-stock products.

### Specification

```python
def low_stock_report(self) -> str:
    """Generate a report of products below the reorder threshold.

    Returns a formatted string like:
        LOW STOCK ALERT
        ===============
        EL-002  Wireless Mouse         qty: 8
        CL-002  Work Gloves            qty: 5
        ---------------
        Total: 2 products need restocking
    
    If no products are low stock, return:
        LOW STOCK ALERT
        ===============
        All products are sufficiently stocked.
    """
```

- Use the store's `low_stock_products()` method
- Format each product line with SKU (left-aligned, 8 chars), name (left-aligned, 25 chars), and quantity
- Include a total count at the bottom

---

## Tests

Tests for both tasks are provided in `tests/test_tasks.py`. Run them to validate your implementation:

```bash
python -m pytest tests/test_tasks.py -v
```
