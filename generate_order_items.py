import mysql.connector
import random

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
# 2. Get existing Orders
# -----------------------------------

cursor.execute("SELECT order_id FROM orders")

order_ids = [row[0] for row in cursor.fetchall()]

print(f"Found {len(order_ids)} orders.")

# -----------------------------------
# 3. Get existing Products
# -----------------------------------

cursor.execute("""
    SELECT product_id, price
    FROM products
""")

products = cursor.fetchall()

print(f"Found {len(products)} products.")

# -----------------------------------
# 4. Generate Order Items
# -----------------------------------

order_items = []

order_item_id = 1

for order_id in order_ids:

    # Each order contains 1–5 products
    number_of_products = random.randint(1, 5)

    # Pick unique products for this order
    selected_products = random.sample(
        products,
        number_of_products
    )

    for product_id, price in selected_products:

        # Quantity purchased
        quantity = random.randint(1, 4)

        # Discount percentage
        discount = random.choice(
            [0, 5, 10, 15, 20]
        )

        # Selling price after discount
        selling_price = round(
            price * (1 - int(discount / 100)),
            2
        )

        order_items.append(
            (
                order_item_id,
                order_id,
                product_id,
                quantity,
                selling_price,
                discount
            )
        )

        order_item_id += 1

# -----------------------------------
# 5. Insert into MySQL
# -----------------------------------

query = """
INSERT IGNORE INTO order_items
(
    order_item_id,
    order_id,
    product_id,
    quantity,
    selling_price,
    discount
)
VALUES (%s, %s, %s, %s, %s, %s)
"""

cursor.executemany(query, order_items)

connection.commit()

print(
    f"{cursor.rowcount} order items inserted successfully!"
)

# -----------------------------------
# 6. Close connection
# -----------------------------------

cursor.close()
connection.close()

print("Order item generation completed!")