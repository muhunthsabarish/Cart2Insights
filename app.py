
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Cart2Insights Analytics",
    page_icon="🛒",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
DATA = BASE_DIR

orders = pd.read_csv(DATA / "orders_with_features.csv")
customers = pd.read_csv(DATA / "customer_features.csv")
sellers = pd.read_csv(DATA / "seller_features.csv")


st.title("🛒 Cart2Insights Analytics")
st.caption("Decoding E-Commerce Performance")

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Explore Dashboard",
    [
        "Business Overview",
        "Sales Analysis",
        "Customer Analysis",
        "Seller & Product Analysis",
        "Delivery Analysis",
        "Customer Experience"
    ]
)

if page == "Business Overview":
    st.header("Business Overview")

    total_revenue = orders["total_order_value"].sum()
    total_orders = orders["order_id"].nunique()
    total_customers = customers["customer_unique_id"].nunique()
    total_sellers = sellers["seller_id"].nunique()
    aov = total_revenue / total_orders if total_orders else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Revenue", f"R$ {total_revenue:,.2f}")
    c2.metric("Total Orders", f"{total_orders:,}")
    c3.metric("Total Customers", f"{total_customers:,}")

    c4, c5 = st.columns(2)
    c4.metric("Total Sellers", f"{total_sellers:,}")
    c5.metric("Average Order Value", f"R$ {aov:,.2f}")

    st.subheader("Order Status")
    status = orders["order_status"].value_counts()
    st.bar_chart(status)

elif page == "Sales Analysis":
    st.header("Sales Analysis")
    monthly = orders.copy()
    monthly["purchase_date"] = pd.to_datetime(
        monthly["order_purchase_timestamp"], errors="coerce"
    )
    monthly = monthly.dropna(subset=["purchase_date"])
    monthly["Month"] = monthly["purchase_date"].dt.to_period("M").astype(str)
    sales = monthly.groupby("Month")["total_order_value"].sum()
    st.subheader("Monthly Sales")
    st.line_chart(sales)
    st.metric("Total Item-Price Sales", f"R$ {orders['total_order_value'].sum():,.2f}")

elif page == "Customer Analysis":
    st.header("Customer Analysis")
    c1, c2 = st.columns(2)
    c1.metric("Total Customers", f"{len(customers):,}")
    c2.metric("Repeat Customers", f"{customers['is_repeat_customer'].sum():,}")
    st.subheader("Customer Spending Distribution")
    st.bar_chart(customers["total_spending"].clip(upper=customers["total_spending"].quantile(0.95)))

elif page == "Seller & Product Analysis":
    st.header("Seller & Product Analysis")
    st.subheader("Top 10 Sellers by Item-Price Revenue")
    top = sellers.nlargest(10, "seller_revenue").set_index("seller_id")
    st.bar_chart(top["seller_revenue"])
    st.metric("Total Sellers", f"{len(sellers):,}")

elif page == "Delivery Analysis":
    st.header("Delivery Analysis")
    delivery = orders.dropna(subset=["delivery_days", "delivery_delay_days"]).copy()
    st.metric("Orders with Valid Delivery Dates", f"{len(delivery):,}")
    st.metric("Average Delivery Days", f"{delivery['delivery_days'].mean():.1f}")
    st.metric("Delayed Orders", f"{delivery['is_delayed'].astype(str).str.lower().eq('true').sum():,}")
    st.subheader("Delivery Time Distribution")
    st.histogram if False else None
    st.bar_chart(delivery["delivery_days"].round().value_counts().sort_index())

elif page == "Customer Experience":
    st.header("Customer Experience")
    reviews = pd.read_csv(
        DATA / "olist_order_reviews_dataset.csv"
    )
    c1, c2 = st.columns(2)
    c1.metric("Total Reviews", f"{len(reviews):,}")
    c2.metric("Average Review Score", f"{reviews['review_score'].mean():.2f} / 5")
    st.subheader("Review Score Distribution")
    st.bar_chart(reviews["review_score"].value_counts().sort_index())


st.sidebar.success("Cart2Insights Dashboard")
