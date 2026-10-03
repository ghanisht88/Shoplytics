import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import os


# ==========================================================
# 1. CONNECT TO MYSQL
# ==========================================================

connection = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",
    password="ghanisht",
    database="shoplytics"
)

print("Connected to Shoplytics!")


# ==========================================================
# 2. CREATE OUTPUT FOLDER
# ==========================================================

os.makedirs("charts", exist_ok=True)


# ==========================================================
# 3. LOAD SALES DATA
# ==========================================================

query = """
SELECT
    oi.order_id,
    oi.product_id,
    oi.quantity,
    oi.selling_price,
    oi.discount,

    o.customer_id,
    o.order_date,
    o.order_status,

    p.product_name,
    p.cost,

    c.category_name

FROM order_items oi

JOIN orders o
    ON oi.order_id = o.order_id

JOIN products p
    ON oi.product_id = p.product_id

JOIN categories c
    ON p.category_id = c.category_id;
"""

sales = pd.read_sql(query, connection)


# ==========================================================
# 4. CALCULATE REVENUE & PROFIT
# ==========================================================

sales["revenue"] = (
    sales["quantity"] *
    sales["selling_price"]
)

sales["cost_amount"] = (
    sales["quantity"] *
    sales["cost"]
)

sales["profit"] = (
    sales["revenue"] -
    sales["cost_amount"]
)


# ==========================================================
# 5. MONTHLY SALES
# ==========================================================

sales["order_date"] = pd.to_datetime(
    sales["order_date"]
)

sales["month"] = (
    sales["order_date"]
    .dt.to_period("M")
)

monthly_sales = (
    sales
    .groupby("month")
    .agg(
        revenue=("revenue", "sum"),
        orders=("order_id", "nunique")
    )
    .reset_index()
)


# ==========================================================
# 6. TOP PRODUCTS
# ==========================================================

top_products = (
    sales
    .groupby(
        ["product_id", "product_name"]
    )
    .agg(
        quantity_sold=("quantity", "sum"),
        revenue=("revenue", "sum")
    )
    .reset_index()
    .sort_values(
        "quantity_sold",
        ascending=False
    )
)


# ==========================================================
# 7. CATEGORY ANALYSIS
# ==========================================================

category_analysis = (
    sales
    .groupby("category_name")
    .agg(
        products_sold=("quantity", "sum"),
        revenue=("revenue", "sum"),
        profit=("profit", "sum")
    )
    .reset_index()
    .sort_values(
        "revenue",
        ascending=False
    )
)


# ==========================================================
# 8. PAYMENT ANALYSIS
# ==========================================================

payment_query = """
SELECT
    payment_method,
    payment_status,
    amount
FROM payments;
"""

payments = pd.read_sql(
    payment_query,
    connection
)

payment_method_analysis = (
    payments
    .groupby("payment_method")
    .agg(
        transactions=("payment_method", "count"),
        amount=("amount", "sum")
    )
    .reset_index()
    .sort_values(
        "transactions",
        ascending=False
    )
)


# ==========================================================
# 9. CUSTOMER ANALYSIS
# ==========================================================

customer_analysis = (
    sales
    .groupby(
        ["customer_id"]
    )
    .agg(
        orders=("order_id", "nunique"),
        revenue=("revenue", "sum")
    )
    .reset_index()
    .sort_values(
        "revenue",
        ascending=False
    )
)


# ==========================================================
# 10. CHART 1 — MONTHLY REVENUE
# ==========================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales["month"].astype(str),
    monthly_sales["revenue"],
    marker="o"
)

plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue (Rs.)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "charts/monthly_revenue.png"
)

plt.close()


# ==========================================================
# 11. CHART 2 — TOP PRODUCTS
# ==========================================================

top_10_products = (
    top_products
    .head(10)
    .sort_values("quantity_sold")
)

plt.figure(figsize=(10, 6))

plt.barh(
    top_10_products["product_name"],
    top_10_products["quantity_sold"]
)

plt.title("Top 10 Best-Selling Products")
plt.xlabel("Quantity Sold")
plt.ylabel("Product")

plt.tight_layout()

plt.savefig(
    "charts/top_products.png"
)

plt.close()


# ==========================================================
# 12. CHART 3 — CATEGORY REVENUE
# ==========================================================

plt.figure(figsize=(9, 6))

plt.bar(
    category_analysis["category_name"],
    category_analysis["revenue"]
)

plt.title("Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Revenue (Rs.)")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    "charts/category_revenue.png"
)

plt.close()


# ==========================================================
# 13. CHART 4 — CATEGORY PROFIT
# ==========================================================

plt.figure(figsize=(9, 6))

plt.bar(
    category_analysis["category_name"],
    category_analysis["profit"]
)

plt.title("Profit by Category")
plt.xlabel("Category")
plt.ylabel("Profit (Rs.)")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    "charts/category_profit.png"
)

plt.close()


# ==========================================================
# 14. CHART 5 — PAYMENT METHODS
# ==========================================================

plt.figure(figsize=(9, 6))

plt.bar(
    payment_method_analysis["payment_method"],
    payment_method_analysis["transactions"]
)

plt.title("Payment Method Usage")
plt.xlabel("Payment Method")
plt.ylabel("Number of Transactions")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    "charts/payment_methods.png"
)

plt.close()


# ==========================================================
# 15. CHART 6 — TOP CUSTOMERS
# ==========================================================

top_10_customers = (
    customer_analysis
    .head(10)
    .sort_values("revenue")
)

plt.figure(figsize=(10, 6))

plt.barh(
    top_10_customers["customer_id"].astype(str),
    top_10_customers["revenue"]
)

plt.title("Top 10 Customers by Revenue")
plt.xlabel("Revenue (Rs.)")
plt.ylabel("Customer ID")

plt.tight_layout()

plt.savefig(
    "charts/top_customers.png"
)

plt.close()


# ==========================================================
# 16. FINISH
# ==========================================================

connection.close()

print("\n" + "=" * 60)
print("           VISUALIZATION COMPLETED")
print("=" * 60)

print("Charts created successfully:")

print("1. monthly_revenue.png")
print("2. top_products.png")
print("3. category_revenue.png")
print("4. category_profit.png")
print("5. payment_methods.png")
print("6. top_customers.png")

print("\nCharts are saved inside the 'charts' folder.")