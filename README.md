# Python Example Case – Student Worker Candidate Test

Welcome! This exercise is designed to evaluate your ability to **read, understand, and reason about** Python code. There are no trick questions — we want to see how you think.

## What You'll Do

1. **Read** the provided Python code in the `inventory/` package
2. **Implement** two small tasks described in `TASKS.md`
3. **Run** the tests to verify your implementation: `python -m pytest tests/`

## Project Overview

The codebase is a small **warehouse inventory system** that:

- Tracks products with quantities and categories
- Supports adding, removing, and searching products
- Generates simple inventory reports
- Reads/writes data from CSV files

The code is intentionally small but uses several Python patterns and design choices worth discussing.

## Getting Started

```bash
# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Run the existing tests
python -m pytest tests/ -v

# Run the application
python -m inventory --help
```

## Deliverables

1. Your code changes for the tasks in `TASKS.md`
2. All tests passing: `python -m pytest tests/ -v`

Good luck!
