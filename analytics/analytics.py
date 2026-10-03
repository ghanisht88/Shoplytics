import mysql.connector
import pandas as pd


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

print("=" * 60)
print("          SHOPLYTICS ANALYTICS SYSTEM")
print("=" * 60)

print("\nConnected to Shoplytics database!")


# ==========================================================
# 2. LOAD SALES DATA
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
# 3. CALCULATE REVENUE AND PROFIT
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
# 4. BASIC SALES KPIs
# ==========================================================

total_revenue = sales["revenue"].sum()

total_orders = sales["order_id"].nunique()

total_customers = sales["customer_id"].nunique()

total_products_sold = sales["quantity"].sum()

average_order_value = (
    total_revenue / total_orders
)


print("\n" + "=" * 60)
print("                    SALES KPIs")
print("=" * 60)

print(f"Total Revenue       : Rs.{total_revenue:,.2f}")
print(f"Total Orders        : {total_orders:,}")
print(f"Total Customers     : {total_customers:,}")
print(f"Products Sold       : {total_products_sold:,}")
print(f"Average Order Value : Rs.{average_order_value:,.2f}")


# ==========================================================
# 5. MONTHLY SALES ANALYSIS
# ==========================================================

sales["order_date"] = pd.to_datetime(
    sales["order_date"]
)

sales["month"] = (
    sales["order_date"]
    .dt.to_period("M")
)

monthly_sales = (
    sales.groupby("month")
    .agg(
        revenue=("revenue", "sum"),
        orders=("order_id", "nunique"),
        products_sold=("quantity", "sum")
    )
    .reset_index()
)

monthly_sales["growth_%"] = (
    monthly_sales["revenue"]
    .pct_change()
    * 100
)

monthly_sales["growth_%"] = (
    monthly_sales["growth_%"].round(2)
)


print("\n" + "=" * 60)
print("                 MONTHLY SALES")
print("=" * 60)

print(monthly_sales.to_string(index=False))


# ==========================================================
# 6. BEST SALES MONTH
# ==========================================================

best_month = monthly_sales.loc[
    monthly_sales["revenue"].idxmax()
]

print("\nBest Sales Month:")
print(
    f"{best_month['month']} = "
    f"Rs.{best_month['revenue']:,.2f}"
)


# ==========================================================
# 7. TOP PRODUCTS BY QUANTITY
# ==========================================================

top_products = (
    sales.groupby(
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

print("\n" + "=" * 60)
print("              TOP 10 SELLING PRODUCTS")
print("=" * 60)

print(
    top_products
    .head(10)
    .to_string(index=False)
)


# ==========================================================
# 8. TOP PRODUCTS BY REVENUE
# ==========================================================

top_revenue_products = (
    sales.groupby(
        ["product_id", "product_name"]
    )["revenue"]
    .sum()
    .reset_index()
    .sort_values(
        "revenue",
        ascending=False
    )
)

print("\n" + "=" * 60)
print("             TOP 10 PRODUCTS BY REVENUE")
print("=" * 60)

print(
    top_revenue_products
    .head(10)
    .to_string(index=False)
)


# ==========================================================
# 9. CATEGORY ANALYSIS
# ==========================================================

category_analysis = (
    sales.groupby("category_name")
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

total_category_revenue = (
    category_analysis["revenue"].sum()
)

category_analysis["revenue_percentage"] = (
    category_analysis["revenue"]
    / total_category_revenue
    * 100
)

category_analysis["revenue_percentage"] = (
    category_analysis["revenue_percentage"]
    .round(2)
)


print("\n" + "=" * 60)
print("                 CATEGORY ANALYSIS")
print("=" * 60)

print(
    category_analysis.to_string(index=False)
)


# ==========================================================
# 10. BEST CATEGORY
# ==========================================================

best_category = category_analysis.iloc[0]

print("\nBest Performing Category:")

print(
    f"{best_category['category_name']} "
    f"= Rs.{best_category['revenue']:,.2f}"
)


# ==========================================================
# 11. PROFIT ANALYSIS
# ==========================================================

total_cost = sales["cost_amount"].sum()

total_profit = sales["profit"].sum()

profit_margin = (
    total_profit / total_revenue
) * 100


print("\n" + "=" * 60)
print("                  PROFIT ANALYSIS")
print("=" * 60)

print(f"Total Revenue : Rs.{total_revenue:,.2f}")
print(f"Total Cost    : Rs.{total_cost:,.2f}")
print(f"Total Profit  : Rs.{total_profit:,.2f}")
print(f"Profit Margin : {profit_margin:.2f}%")


# ==========================================================
# 12. CUSTOMER ANALYSIS
# ==========================================================

customer_query = """
SELECT
    c.customer_id,
    c.customer_name,
    c.city,
    o.order_id,
    o.order_date,
    oi.product_id,
    oi.quantity,
    oi.selling_price,
    p.cost

FROM customers c

JOIN orders o
    ON c.customer_id = o.customer_id

JOIN order_items oi
    ON o.order_id = oi.order_id

JOIN products p
    ON oi.product_id = p.product_id;
"""

customer_data = pd.read_sql(
    customer_query,
    connection
)


# Calculate revenue and profit

customer_data["revenue"] = (
    customer_data["quantity"] *
    customer_data["selling_price"]
)

customer_data["cost"] = (
    customer_data["quantity"] *
    customer_data["cost"]
)

customer_data["profit"] = (
    customer_data["revenue"] -
    customer_data["cost"]
)


# ----------------------------------------------------------
# Customer performance
# ----------------------------------------------------------

customer_analysis = (
    customer_data
    .groupby(
        ["customer_id", "customer_name", "city"]
    )
    .agg(
        orders=("order_id", "nunique"),
        products_purchased=("quantity", "sum"),
        revenue=("revenue", "sum"),
        profit=("profit", "sum")
    )
    .reset_index()
)


# Average Order Value for each customer

customer_analysis["average_order_value"] = (
    customer_analysis["revenue"] /
    customer_analysis["orders"]
)


customer_analysis["average_order_value"] = (
    customer_analysis["average_order_value"]
    .round(2)
)


# ----------------------------------------------------------
# Top customers by revenue
# ----------------------------------------------------------

top_customers = (
    customer_analysis
    .sort_values(
        "revenue",
        ascending=False
    )
)


print("\n" + "=" * 60)
print("              TOP 10 CUSTOMERS")
print("=" * 60)

print(
    top_customers[
        [
            "customer_id",
            "customer_name",
            "city",
            "orders",
            "products_purchased",
            "revenue",
            "profit"
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# ----------------------------------------------------------
# Repeat customers
# ----------------------------------------------------------

repeat_customers = customer_analysis[
    customer_analysis["orders"] > 1
]

print("\n" + "=" * 60)
print("              CUSTOMER STATISTICS")
print("=" * 60)

print(
    f"Total Customers with Orders : "
    f"{len(customer_analysis):,}"
)

print(
    f"Repeat Customers             : "
    f"{len(repeat_customers):,}"
)

print(
    f"One-Time Customers           : "
    f"{len(customer_analysis[customer_analysis['orders'] == 1]):,}"
)


# ----------------------------------------------------------
# Highest-value customer
# ----------------------------------------------------------

highest_value_customer = (
    customer_analysis
    .loc[customer_analysis["revenue"].idxmax()]
)

print("\nHighest Value Customer:")

print(
    f"{highest_value_customer['customer_name']} "
    f"= Rs.{highest_value_customer['revenue']:,.2f}"
)


# ==========================================================
# 13. PAYMENT ANALYSIS
# ==========================================================

payment_query = """
SELECT
    p.payment_id,
    p.order_id,
    p.payment_date,
    p.payment_method,
    p.payment_status,
    p.amount
FROM payments p;
"""

payments = pd.read_sql(
    payment_query,
    connection
)


# ----------------------------------------------------------
# Payment method analysis
# ----------------------------------------------------------

payment_method_analysis = (
    payments
    .groupby("payment_method")
    .agg(
        transactions=("payment_id", "count"),
        amount=("amount", "sum")
    )
    .reset_index()
    .sort_values(
        "amount",
        ascending=False
    )
)


print("\n" + "=" * 60)
print("              PAYMENT METHOD ANALYSIS")
print("=" * 60)

print(
    payment_method_analysis
    .to_string(index=False)
)


# ----------------------------------------------------------
# Payment status analysis
# ----------------------------------------------------------

payment_status_analysis = (
    payments
    .groupby("payment_status")
    .agg(
        transactions=("payment_id", "count"),
        amount=("amount", "sum")
    )
    .reset_index()
)


print("\n" + "=" * 60)
print("              PAYMENT STATUS ANALYSIS")
print("=" * 60)

print(
    payment_status_analysis
    .to_string(index=False)
)


# ----------------------------------------------------------
# Most popular payment method
# ----------------------------------------------------------

popular_payment_method = (
    payment_method_analysis
    .loc[
        payment_method_analysis["transactions"].idxmax()
    ]
)

print("\nMost Popular Payment Method:")

print(
    f"{popular_payment_method['payment_method']} "
    f"= {popular_payment_method['transactions']:,} transactions"
)


# ----------------------------------------------------------
# Successful payments
# ----------------------------------------------------------

successful_payments = payments[
    payments["payment_status"] == "Completed"
]

failed_payments = payments[
    payments["payment_status"] == "Failed"
]

print("\nPayment Summary:")

print(
    f"Completed Payments : "
    f"{len(successful_payments):,}"
)

print(
    f"Failed Payments    : "
    f"{len(failed_payments):,}"
)


# ----------------------------------------------------------
# Payment success rate
# ----------------------------------------------------------

total_payment_transactions = len(payments)

payment_success_rate = (
    len(successful_payments)
    / total_payment_transactions
    * 100
)

print(
    f"Payment Success Rate: "
    f"{payment_success_rate:.2f}%"
)


# ==========================================================
# 14. PROFIT & BUSINESS ANALYSIS
# ==========================================================

# ----------------------------------------------------------
# Overall Profit
# ----------------------------------------------------------

total_revenue = sales["revenue"].sum()
total_cost = sales["cost"].sum()
total_profit = sales["profit"].sum()

profit_margin = (
    total_profit / total_revenue
) * 100


print("\n" + "=" * 60)
print("             PROFIT & BUSINESS ANALYSIS")
print("=" * 60)

print(f"Total Revenue : Rs.{total_revenue:,.2f}")
print(f"Total Cost    : Rs.{total_cost:,.2f}")
print(f"Total Profit  : Rs.{total_profit:,.2f}")
print(f"Profit Margin : {profit_margin:.2f}%")


# ----------------------------------------------------------
# Top Products by Profit
# ----------------------------------------------------------

product_profit = (
    sales
    .groupby(
        ["product_id", "product_name"]
    )
    .agg(
        revenue=("revenue", "sum"),
        cost=("cost", "sum"),
        profit=("profit", "sum"),
        quantity_sold=("quantity", "sum")
    )
    .reset_index()
    .sort_values(
        "profit",
        ascending=False
    )
)

print("\n" + "=" * 60)
print("           TOP 10 PRODUCTS BY PROFIT")
print("=" * 60)

print(
    product_profit
    .head(10)
    .to_string(index=False)
)


# ----------------------------------------------------------
# Category Profit Analysis
# ----------------------------------------------------------

category_profit = (
    sales
    .groupby("category_name")
    .agg(
        revenue=("revenue", "sum"),
        cost=("cost", "sum"),
        profit=("profit", "sum")
    )
    .reset_index()
)

category_profit["profit_margin_%"] = (
    category_profit["profit"]
    / category_profit["revenue"]
    * 100
)

category_profit["profit_margin_%"] = (
    category_profit["profit_margin_%"]
    .round(2)
)

category_profit = category_profit.sort_values(
    "profit",
    ascending=False
)


print("\n" + "=" * 60)
print("             CATEGORY PROFIT ANALYSIS")
print("=" * 60)

print(
    category_profit
    .to_string(index=False)
)


# ----------------------------------------------------------
# Most Profitable Category
# ----------------------------------------------------------

most_profitable_category = (
    category_profit.iloc[0]
)

print("\nMost Profitable Category:")

print(
    f"{most_profitable_category['category_name']} "
    f"= Rs.{most_profitable_category['profit']:,.2f}"
)


# ----------------------------------------------------------
# Highest Profit Product
# ----------------------------------------------------------

highest_profit_product = (
    product_profit.iloc[0]
)

print("\nMost Profitable Product:")

print(
    f"{highest_profit_product['product_name']} "
    f"= Rs.{highest_profit_product['profit']:,.2f}"
)

# ==========================================================
# 15. CLOSE CONNECTION
# ==========================================================

connection.close()

print("\n" + "=" * 60)
print("           SHOPLYTICS ANALYSIS COMPLETED")
print("=" * 60)