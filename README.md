# Financial Transaction Pipeline

## Overview
Automated system for processing bank transactions with fraud detection and merchant validation.

## Features
- Transaction fraud detection
- Customer profile enrichment
- Merchant blacklist validation
- Automated reporting

## Setup
```bash
pip install -r requirements.txt
```

## Usage
```bash
python scripts/processor.py
python scripts/enricher.py
python scripts/validator.py
```

## Output Files
- `outputs/flagged_transactions.csv` - Suspicious transactions
- `outputs/enriched_transactions.csv` - Transactions with customer data
- `outputs/blocked_transactions.csv` - Blacklisted merchants
- `outputs/report.txt` - Summary report
