import psycopg
from faker import Faker
from oltp_client import DSN  # reuse the DSN from your client

fake = Faker()

def update_customer_names():
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT customer_id FROM customers;")
            customer_ids = [row[0] for row in cur.fetchall()]

            for cid in customer_ids:
                new_name = fake.name()
                cur.execute(
                    "UPDATE customers SET name=%s WHERE customer_id=%s;",
                    (new_name, cid)
                )
        conn.commit()

if __name__ == "__main__":
    update_customer_names()
    print("Customer names updated with realistic names!")
