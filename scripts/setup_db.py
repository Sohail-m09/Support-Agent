"""
setup_db.py - one-time script: creates the tables and loads the fake orders.

Run from the project root:   python -m scripts.setup_db
WARNING: it drops and recreates the tables, so it wipes refund requests
and policy chunks. Use it only for setup or a full reset.
"""
import csv
from datetime import date
from decimal import Decimal

from app import config
from app.db.connection import get_connection

SCHEMA_FILE = config.ROOT_DIR / "app" / "db" / "schema.sql"
ORDERS_FILE = config.ROOT_DIR / "data" / "seed_orders.csv"


def create_tables(conn):
    sql = SCHEMA_FILE.read_text(encoding="utf-8")
    conn.execute(sql)
    print("Tables created.")


def load_orders(conn):
    with open(ORDERS_FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        delivered = row["delivered_date"]  # empty means "not delivered yet"
        conn.execute(
            """
            INSERT INTO orders
                (order_id, customer_id, item, category, price,
                 status, order_date, delivered_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                int(row["order_id"]),
                row["customer_id"],
                row["item"],
                row["category"],
                Decimal(row["price"]),
                row["status"],
                date.fromisoformat(row["order_date"]),
                date.fromisoformat(delivered) if delivered else None,
            ),
        )
    print(f"Loaded {len(rows)} orders.")


def main():
    config.check_required_settings()
    with get_connection() as conn:
        create_tables(conn)
        load_orders(conn)
    print("Database ready.")


if __name__ == "__main__":
    main()