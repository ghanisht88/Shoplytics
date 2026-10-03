import mysql.connector
from fakecustomer import customers

connection=mysql.connector.connect(
    host="localhost",
    user="root",
    port=3307,
    password="ghanisht",
    database="shoplytics"
)

cursor = connection.cursor()

query = """
INSERT INTO customers
(customer_id, customer_name, gender, age, city, registration_date)
VALUES (%s, %s, %s, %s, %s, %s)
"""

for _, row in customers.iterrows():

    cursor.execute(
        query,
        (
            int(row["customer_id"]),
            row["customer_name"],
            row["gender"],
            int(row["age"]),
            row["city"],
            row["registration_date"].date()
        )
    )

connection.commit()

print("Customers inserted successfully!")