import pandas as pd
from datetime import datetime
import sys

def load_transactions(filepath):
    """Load transaction data"""
    df = pd.read_csv(filepath)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def flag_suspicious(df):
    """Flag suspicious transactions"""
    df['is_suspicious'] = False
    
    # Rule 1: Amount > $5000
    df.loc[df['amount'] > 5000, 'is_suspicious'] = True
    
    # Rule 2: Multiple high-value transactions same account within 10 min
    df = df.sort_values(['account_id', 'timestamp'])
    df['time_diff'] = df.groupby('account_id')['timestamp'].diff().dt.total_seconds()
    df.loc[(df['amount'] > 1000) & (df['time_diff'] < 600), 'is_suspicious'] = True
    
    return df

def generate_report(df, output_path):
    """Generate summary report"""
    report = {
        'total_transactions': len(df),
        'total_amount': df['amount'].sum(),
        'suspicious_count': df['is_suspicious'].sum(),
        'suspicious_amount': df[df['is_suspicious']]['amount'].sum(),
        'top_categories': df.groupby('category')['amount'].sum().nlargest(5).to_dict()
    }
    
    with open(output_path, 'w') as f:
        f.write("TRANSACTION ANALYSIS REPORT\n")
        f.write("="*50 + "\n")
        for key, value in report.items():
            f.write(f"{key}: {value}\n")
    
    return report

def main():
    # Process
    df = load_transactions('data/transactions.csv')
    df = flag_suspicious(df)
    
    # Save flagged transactions
    flagged = df[df['is_suspicious']]
    flagged.to_csv('outputs/flagged_transactions.csv', index=False)
    
    # Generate report
    generate_report(df, 'outputs/report.txt')
    
    print(f"Processed {len(df)} transactions")
    print(f"Flagged {len(flagged)} suspicious transactions")

if __name__ == "__main__":
    main()
