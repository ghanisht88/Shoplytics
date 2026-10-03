import mysql.connector
import random
from datetime import date

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
# 2. Get orders
# -----------------------------------

cursor.execute("""
    SELECT order_id, order_date, total_amount
    FROM orders
""")

orders = cursor.fetchall()

print(f"Found {len(orders)} orders.")

# -----------------------------------
# 3. Generate payments
# -----------------------------------

payments = []

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Cash on Delivery"
]

payment_statuses = [
    "Completed",
    "Completed",
    "Completed",
    "Completed",
    "Failed"
]

for payment_id, (order_id, order_date, total_amount) in enumerate(
    orders, start=1
):

    payment_method = random.choice(payment_methods)

    payment_status = random.choice(payment_statuses)

    # For failed payments, amount is 0
    if payment_status == "Failed":
        amount = 0.00
    else:
        amount = total_amount

    payments.append(
        (
            payment_id,
            order_id,
            order_date,
            payment_method,
            payment_status,
            amount
        )
    )

# -----------------------------------
# 4. Insert payments
# -----------------------------------

query = """
INSERT IGNORE INTO payments
(
    payment_id,
    order_id,
    payment_date,
    payment_method,
    payment_status,
    amount
)
VALUES (%s, %s, %s, %s, %s, %s)
"""

cursor.executemany(query, payments)

connection.commit()

print(f"{cursor.rowcount} payments inserted successfully!")

# -----------------------------------
# 5. Close connection
# -----------------------------------

cursor.close()
connection.close()

print("Payment generation completed!")