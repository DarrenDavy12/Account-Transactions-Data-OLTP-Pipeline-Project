import os
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row
from datetime import datetime
from decimal import Decimal
import json

load_dotenv()

DSN = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

def create_customer(conn, email, name):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO customers (email, name) VALUES (%s, %s) ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name RETURNING customer_id;",
            (email, name)
        )
        return cur.fetchone()[0]

def create_account(conn, customer_id, account_type='checking', currency='USD'):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO accounts (customer_id, account_type, currency) VALUES (%s, %s, %s) ON CONFLICT (customer_id, account_type) DO UPDATE SET currency=EXCLUDED.currency RETURNING account_id;",
            (customer_id, account_type, currency)
        )
        return cur.fetchone()[0]

def transaction(conn, account_id, amount, currency='USD', ttype='credit', metadata=None):
    amount = Decimal(str(amount))  # convert float to Decimal
    with conn.transaction():
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO transactions (account_id, amount, currency, type, status, metadata) VALUES (%s,%s,%s,%s,%s,%s) RETURNING transaction_id;",
                (account_id, amount, currency, ttype, 'pending', json.dumps(metadata or {}))
            )
            tx_id = cur.fetchone()[0]

            cur.execute("SELECT balance FROM accounts WHERE account_id = %s FOR UPDATE;", (account_id,))
            row = cur.fetchone()
            if row is None:
                raise Exception("Account not found")
            current_balance = row[0]
            new_balance = current_balance + (amount if ttype == 'credit' else -amount)

            if new_balance < 0:
                cur.execute("UPDATE transactions SET status=%s WHERE transaction_id=%s;", ('failed', tx_id))
                raise Exception("Insufficient funds")

            cur.execute("UPDATE accounts SET balance=%s WHERE account_id=%s;", (new_balance, account_id))
            cur.execute("UPDATE transactions SET status=%s WHERE transaction_id=%s;", ('posted', tx_id))
            return tx_id

def sample_workflow():
    with psycopg.connect(DSN) as conn:
        cid = create_customer(conn, 'alice@example.com', 'Alice')
        aid = create_account(conn, cid, 'checking')
        print("Customer", cid, "Account", aid)
        tx = transaction(conn, aid, 100.00, 'USD', 'credit', {'note': 'initial deposit'})
        print("Posted transaction", tx)

if __name__ == "__main__":
    sample_workflow()
