"""Command-line interface for the inventory system."""

import argparse
from pathlib import Path

from inventory.store import InventoryStore
from inventory.reports import ReportGenerator


def main():
    parser = argparse.ArgumentParser(description="Warehouse Inventory Manager")
    parser.add_argument("--data", "-d", type=str, default="data/products.csv",
                        help="Path to inventory CSV file")
    parser.add_argument("--report", "-r", action="store_true",
                        help="Print an inventory report")
    parser.add_argument("--search", "-s", type=str, default=None,
                        help="Search for a product by name")
    parser.add_argument("--low-stock", action="store_true",
                        help="Show products with low stock")
    args = parser.parse_args()

    store = InventoryStore()
    data_path = Path(args.data)

    if data_path.exists():
        count = store.load_csv(data_path)
        print(f"Loaded {count} products from {data_path}")
    else:
        print(f"Warning: {data_path} not found. Starting with empty inventory.")

    if args.report:
        report = ReportGenerator(store)
        print(report.format_text_report())
    elif args.search:
        results = store.search(args.search)
        if results:
            for p in results:
                print(f"  {p.sku:<12} {p.name:<25} qty={p.quantity:<5} {p.price:>8.2f} DKK")
        else:
            print(f"No products matching '{args.search}'")
    elif args.low_stock:
        low = store.low_stock_products()
        if low:
            print(f"Products below reorder threshold ({len(low)}):")
            for p in low:
                print(f"  {p.sku:<12} {p.name:<25} qty={p.quantity}")
        else:
            print("All products are sufficiently stocked.")
    else:
        print(f"Inventory has {store.count} products. Use --report, --search, or --low-stock.")


if __name__ == "__main__":
    main()
