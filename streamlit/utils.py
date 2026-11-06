
# Cart2Insights - Utility Functions

import pandas as pd


def format_currency(value):
    """Format a numeric value as Brazilian Real."""
    return f"R$ {value:,.2f}"


def format_number(value):
    """Format a number with thousands separators."""
    return f"{value:,.0f}"


def calculate_average_order_value(revenue, orders):
    """Calculate average order value safely."""
    if orders == 0:
        return 0
    return revenue / orders


def prepare_monthly_sales(orders):
    """Prepare monthly sales data for visualization."""
    monthly = orders.copy()

    monthly["purchase_date"] = pd.to_datetime(
        monthly["order_purchase_timestamp"],
        errors="coerce"
    )

    monthly = monthly.dropna(subset=["purchase_date"])

    monthly["Month"] = (
        monthly["purchase_date"].dt.to_period("M").astype(str)
    )

    return monthly.groupby("Month")["total_order_value"].sum()


def get_delivery_summary(orders):
    """Calculate delivery performance using valid delivery records."""
    delivery = orders.dropna(
        subset=["delivery_days", "delivery_delay_days"]
    ).copy()

    average_days = (
        delivery["delivery_days"].mean()
        if not delivery.empty else 0
    )

    delayed_orders = (
        delivery["is_delayed"]
        .astype(str)
        .str.lower()
        .eq("true")
        .sum()
    )

    return {
        "valid_delivery_orders": len(delivery),
        "average_delivery_days": average_days,
        "delayed_orders": delayed_orders
    }


def get_review_summary(reviews):
    """Calculate customer review statistics."""
    return {
        "total_reviews": len(reviews),
        "average_review_score": (
            reviews["review_score"].mean()
            if not reviews.empty else 0
        )
    }
