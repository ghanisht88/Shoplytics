import streamlit as st
import mysql.connector
import pandas as pd


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Shoplytics",
    page_icon="📊",
    layout="wide"
)


# ==========================================================
# TITLE
# ==========================================================

st.title("📊 Shoplytics")
st.subheader("E-Commerce Sales Analytics Dashboard")

st.write(
    "Analyze sales, products, customers, categories, "
    "profit and payment performance."
)


# ==========================================================
# MYSQL CONNECTION
# ==========================================================

@st.cache_resource
def get_connection():

    return mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="ghanisht",
        database="shoplytics"
    )


connection = get_connection()


# ==========================================================
# LOAD SALES DATA
# ==========================================================

@st.cache_data
def load_sales_data():

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

    df = pd.read_sql(query, connection)

    return df


sales = load_sales_data()


# ==========================================================
# CALCULATE REVENUE AND PROFIT
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

sales["order_date"] = pd.to_datetime(
    sales["order_date"]
)


# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

st.sidebar.header("🔎 Filters")


# Date filter

min_date = sales["order_date"].min().date()
max_date = sales["order_date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# Category filter

categories = sorted(
    sales["category_name"].unique()
)

selected_categories = st.sidebar.multiselect(
    "Select Category",
    categories,
    default=categories
)


# Apply filters

if len(date_range) == 2:

    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1])

    filtered_sales = sales[
        (sales["order_date"] >= start_date) &
        (sales["order_date"] <= end_date)
    ]

else:

    filtered_sales = sales


filtered_sales = filtered_sales[
    filtered_sales["category_name"].isin(
        selected_categories
    )
]


# ==========================================================
# KPI CALCULATIONS
# ==========================================================

total_revenue = filtered_sales["revenue"].sum()

total_profit = filtered_sales["profit"].sum()

total_orders = filtered_sales["order_id"].nunique()

total_customers = filtered_sales["customer_id"].nunique()

products_sold = filtered_sales["quantity"].sum()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)


# ==========================================================
# KPI CARDS
# ==========================================================

st.markdown("## 📌 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)


col1.metric(
    "💰 Revenue",
    f"Rs. {total_revenue:,.0f}"
)

col2.metric(
    "📦 Orders",
    f"{total_orders:,}"
)

col3.metric(
    "👥 Customers",
    f"{total_customers:,}"
)

col4.metric(
    "💵 Profit",
    f"Rs. {total_profit:,.0f}"
)

col5.metric(
    "🛒 AOV",
    f"Rs. {average_order_value:,.0f}"
)


st.divider()


# ==========================================================
# MONTHLY SALES TREND
# ==========================================================

st.header("📈 Sales Trend")

monthly_sales = (
    filtered_sales
    .assign(
        month=filtered_sales["order_date"]
        .dt.to_period("M")
        .astype(str)
    )
    .groupby("month")
    .agg(
        Revenue=("revenue", "sum"),
        Orders=("order_id", "nunique")
    )
    .reset_index()
)

st.line_chart(
    monthly_sales.set_index("month")["Revenue"]
)


# ==========================================================
# PRODUCT ANALYSIS
# ==========================================================

st.header("🏆 Product Performance")

product_analysis = (
    filtered_sales
    .groupby("product_name")
    .agg(
        Quantity_Sold=("quantity", "sum"),
        Revenue=("revenue", "sum"),
        Profit=("profit", "sum")
    )
    .reset_index()
)


col1, col2 = st.columns(2)


# Top products by quantity

with col1:

    st.subheader("Top 10 Best-Selling Products")

    top_products = (
        product_analysis
        .sort_values(
            "Quantity_Sold",
            ascending=False
        )
        .head(10)
    )

    st.bar_chart(
        top_products.set_index(
            "product_name"
        )["Quantity_Sold"]
    )


# Top products by revenue

with col2:

    st.subheader("Top 10 Products by Revenue")

    top_revenue_products = (
        product_analysis
        .sort_values(
            "Revenue",
            ascending=False
        )
        .head(10)
    )

    st.bar_chart(
        top_revenue_products.set_index(
            "product_name"
        )["Revenue"]
    )


# ==========================================================
# CATEGORY ANALYSIS
# ==========================================================

st.header("📦 Category Performance")

category_analysis = (
    filtered_sales
    .groupby("category_name")
    .agg(
        Products_Sold=("quantity", "sum"),
        Revenue=("revenue", "sum"),
        Profit=("profit", "sum")
    )
    .reset_index()
)


col1, col2 = st.columns(2)


with col1:

    st.subheader("Revenue by Category")

    st.bar_chart(
        category_analysis.set_index(
            "category_name"
        )["Revenue"]
    )


with col2:

    st.subheader("Profit by Category")

    st.bar_chart(
        category_analysis.set_index(
            "category_name"
        )["Profit"]
    )


# ==========================================================
# CUSTOMER ANALYSIS
# ==========================================================

st.header("👥 Customer Analysis")

customer_analysis = (
    filtered_sales
    .groupby("customer_id")
    .agg(
        Orders=("order_id", "nunique"),
        Products_Purchased=("quantity", "sum"),
        Revenue=("revenue", "sum"),
        Profit=("profit", "sum")
    )
    .reset_index()
)


top_customers = (
    customer_analysis
    .sort_values(
        "Revenue",
        ascending=False
    )
    .head(10)
)


st.subheader("Top 10 Customers")

st.dataframe(
    top_customers,
    use_container_width=True
)


# ==========================================================
# PAYMENT ANALYSIS
# ==========================================================

st.header("💳 Payment Analysis")


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


payment_analysis = (
    payments
    .groupby("payment_method")
    .agg(
        Transactions=("payment_method", "count"),
        Amount=("amount", "sum")
    )
    .reset_index()
)


col1, col2 = st.columns(2)


with col1:

    st.subheader("Payment Method Usage")

    st.bar_chart(
        payment_analysis.set_index(
            "payment_method"
        )["Transactions"]
    )


with col2:

    st.subheader("Payment Amount")

    st.bar_chart(
        payment_analysis.set_index(
            "payment_method"
        )["Amount"]
    )


# ==========================================================
# BUSINESS INSIGHTS
# ==========================================================

st.header("💡 Business Insights")


if not category_analysis.empty:

    best_category = category_analysis.loc[
        category_analysis["Revenue"].idxmax(),
        "category_name"
    ]

    most_profitable_category = category_analysis.loc[
        category_analysis["Profit"].idxmax(),
        "category_name"
    ]

else:

    best_category = "N/A"
    most_profitable_category = "N/A"


if not product_analysis.empty:

    best_product = product_analysis.loc[
        product_analysis["Quantity_Sold"].idxmax(),
        "product_name"
    ]

else:

    best_product = "N/A"


col1, col2, col3 = st.columns(3)


col1.info(
    f"🏆 **Best Category**\n\n"
    f"{best_category}"
)

col2.success(
    f"💰 **Most Profitable Category**\n\n"
    f"{most_profitable_category}"
)

col3.warning(
    f"🔥 **Best-Selling Product**\n\n"
    f"{best_product}"
)


# ==========================================================
# DATA TABLE
# ==========================================================

st.header("📋 Sales Data")

st.dataframe(
    filtered_sales[
        [
            "order_id",
            "customer_id",
            "product_name",
            "category_name",
            "quantity",
            "selling_price",
            "revenue",
            "profit",
            "order_date"
        ]
    ],
    use_container_width=True
)


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "Shoplytics | E-Commerce Sales Analytics System | "
    "Built with Python, MySQL, Pandas and Streamlit"
)