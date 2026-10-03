import mysql.connector
import random
from datetime import date, timedelta

# -----------------------------------
# 1. Connect to MySQL
# -----------------------------------

connection = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",
    password="ghanisht",
    database="shoplytics"
)

cursor = connection.cursor()

# -----------------------------------
# 2. Get existing customer IDs
# -----------------------------------

cursor.execute("SELECT customer_id FROM customers")

customer_ids = [row[0] for row in cursor.fetchall()]

print(f"Found {len(customer_ids)} customers.")

# -----------------------------------
# 3. Generate orders
# -----------------------------------

orders = []

start_date = date(2024, 1, 1)
end_date = date(2026, 8, 31)

date_range = (end_date - start_date).days

statuses = [
    "Delivered",
    "Delivered",
    "Delivered",
    "Delivered",
    "Shipped",
    "Processing",
    "Cancelled",
    "Returned"
]

for order_id in range(1, 2001):

    # Select an existing customer
    customer_id = random.choice(customer_ids)

    # Generate random order date
    order_date = start_date + timedelta(
        days=random.randint(0, date_range)
    )

    # Generate order status
    order_status = random.choice(statuses)

    # We will calculate the actual amount later
    # from order_items.
    total_amount = 0.00

    orders.append(
        (
            order_id,
            customer_id,
            order_date,
            order_status,
            total_amount
        )
    )

# -----------------------------------
# 4. Insert orders
# -----------------------------------

query = """
INSERT IGNORE INTO orders
(order_id, customer_id, order_date, order_status, total_amount)
VALUES (%s, %s, %s, %s, %s)
"""

cursor.executemany(query, orders)

connection.commit()

print(f"{cursor.rowcount} new orders inserted.")

# -----------------------------------
# 5. Close connection
# -----------------------------------

cursor.close()
connection.close()

print("Order generation completed!")