
import streamlit as st
import pandas as pd

from database import load_dashboard_data, load_reviews_data
from utils import (
    format_currency,
    get_delivery_summary,
    get_review_summary,
    prepare_monthly_sales
)

st.set_page_config(
    page_title="Cart2Insights Analytics",
    page_icon="🛒",
    layout="wide"
)


@st.cache_data
def load_data():
    return load_dashboard_data()


@st.cache_data
def load_reviews():
    return load_reviews_data()


try:
    orders, customers, sellers = load_data()
except Exception as error:
    st.error(f"Unable to load dashboard datasets: {error}")
    st.stop()


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

    aov = (
        total_revenue / total_orders
        if total_orders else 0
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Revenue", format_currency(total_revenue))
    c2.metric("Total Orders", f"{total_orders:,}")
    c3.metric("Total Customers", f"{total_customers:,}")

    c4, c5 = st.columns(2)

    c4.metric("Total Sellers", f"{total_sellers:,}")
    c5.metric("Average Order Value", format_currency(aov))

    st.subheader("Order Status")

    status = orders["order_status"].value_counts()
    st.bar_chart(status)


elif page == "Sales Analysis":

    st.header("Sales Analysis")

    sales = prepare_monthly_sales(orders)

    st.subheader("Monthly Sales")
    st.line_chart(sales)

    st.metric(
        "Total Item-Price Sales",
        format_currency(orders["total_order_value"].sum())
    )


elif page == "Customer Analysis":

    st.header("Customer Analysis")

    c1, c2 = st.columns(2)

    c1.metric("Total Customers", f"{len(customers):,}")

    c2.metric(
        "Repeat Customers",
        f"{customers['is_repeat_customer'].sum():,}"
    )

    st.subheader("Customer Spending Distribution")

    spending = customers["total_spending"].clip(
        upper=customers["total_spending"].quantile(0.95)
    )

    st.bar_chart(spending)


elif page == "Seller & Product Analysis":

    st.header("Seller & Product Analysis")

    st.subheader("Top 10 Sellers by Item-Price Revenue")

    top = sellers.nlargest(
        10, "seller_revenue"
    ).set_index("seller_id")

    st.bar_chart(top["seller_revenue"])

    st.metric("Total Sellers", f"{len(sellers):,}")


elif page == "Delivery Analysis":

    st.header("Delivery Analysis")

    summary = get_delivery_summary(orders)

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Valid Delivery Orders",
        f"{summary['valid_delivery_orders']:,}"
    )

    c2.metric(
        "Average Delivery Days",
        f"{summary['average_delivery_days']:.1f}"
    )

    c3.metric(
        "Delayed Orders",
        f"{summary['delayed_orders']:,}"
    )

    delivery = orders.dropna(
        subset=["delivery_days", "delivery_delay_days"]
    )

    st.subheader("Delivery Time Distribution")

    st.bar_chart(
        delivery["delivery_days"].round().value_counts().sort_index()
    )


elif page == "Customer Experience":

    st.header("Customer Experience")

    try:
        reviews = load_reviews()

        review_summary = get_review_summary(reviews)

        c1, c2 = st.columns(2)

        c1.metric(
            "Total Reviews",
            f"{review_summary['total_reviews']:,}"
        )

        c2.metric(
            "Average Review Score",
            f"{review_summary['average_review_score']:.2f} / 5"
        )

        st.subheader("Review Score Distribution")

        st.bar_chart(
            reviews["review_score"].value_counts().sort_index()
        )

    except Exception as error:
        st.error(f"Unable to load review data: {error}")


st.sidebar.success("Cart2Insights Dashboard")
