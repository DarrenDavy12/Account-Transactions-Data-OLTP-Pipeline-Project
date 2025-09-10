import random 
from decimal import Decimal 
from oltp_client import create_customer, create_account, transaction, psycopg, DSN


NUM_CUSTOMERS = 50 
ACCOUNTS_PER_CUSTOMER = 2
TRANSACTIONS_PER_ACCOUNT = 10 

def generate_synthetic_data():
    with psycopg.connect(DSN) as conn:
        for i in range(1, NUM_CUSTOMERS + 1):
            email = f"User{i}@example.com"
            name = f"User{i}"
            customer_id = create_customer(conn, email, name)

            for j in range(1, ACCOUNTS_PER_CUSTOMER + 1):
                account_type = random.choice(['checking', 'savings'])
                account_id = create_account(conn, customer_id, account_type)
                

            for k in range(TRANSACTIONS_PER_ACCOUNT):
                amount = Decimal(str(round(random.uniform(10, 500), 2)))
                ttype = random.choice(['credit', 'debit'])
                try:
                    transaction(conn, account_id, amount, ttype=ttype, metadata={'note': f'Synthenic tx {k+1}'})
                except Exception as e:
                        # skip failed transactions (e.g., insufficient funds)
                        print(f"Skipped transaction: {e}")

if __name__ == "__main__":
    generate_synthetic_data()
    print("Synthetic OLTP data generation complete!")