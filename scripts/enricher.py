import pandas as pd
import json

def load_customers(filepath):
    """Load customer profiles"""
    with open(filepath, 'r') as f:
        return pd.DataFrame(json.load(f))

def enrich_transactions(transactions_path, customers_path, output_path):
    """Merge transaction and customer data"""
    txn = pd.read_csv(transactions_path)
    customers = load_customers(customers_path)
    
    # Merge
    enriched = txn.merge(customers, on='account_id', how='left')
    
    # Add risk score
    enriched['risk_score'] = 0
    enriched.loc[enriched['risk_level'] == 'medium', 'risk_score'] = 5
    enriched.loc[enriched['risk_level'] == 'high', 'risk_score'] = 10
    enriched.loc[enriched['amount'] > enriched['avg_monthly_spend'] * 2, 'risk_score'] += 5
    
    enriched.to_csv(output_path, index=False)
    print(f"Enriched {len(enriched)} transactions")
    
    return enriched

if __name__ == "__main__":
    enrich_transactions(
        'data/transactions.csv',
        'data/customers.json',
        'outputs/enriched_transactions.csv'
    )
