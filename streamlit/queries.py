
# Cart2Insights - SQL Analysis Queries

BUSINESS_OVERVIEW_QUERY = """
SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(total_order_value) AS total_revenue
FROM orders_with_features;
"""

MONTHLY_SALES_QUERY = """
SELECT
    strftime('%Y-%m', order_purchase_timestamp) AS month,
    SUM(total_order_value) AS monthly_revenue
FROM orders_with_features
WHERE order_purchase_timestamp IS NOT NULL
GROUP BY month
ORDER BY month;
"""

ORDER_STATUS_QUERY = """
SELECT
    order_status,
    COUNT(DISTINCT order_id) AS total_orders
FROM orders_with_features
GROUP BY order_status
ORDER BY total_orders DESC;
"""

TOP_SELLERS_QUERY = """
SELECT
    seller_id,
    seller_revenue,
    seller_order_count
FROM seller_features
ORDER BY seller_revenue DESC
LIMIT 10;
"""

CUSTOMER_SPENDING_QUERY = """
SELECT
    customer_unique_id,
    total_spending,
    order_count,
    is_repeat_customer
FROM customer_features
ORDER BY total_spending DESC
LIMIT 10;
"""

DELIVERY_PERFORMANCE_QUERY = """
SELECT
    AVG(delivery_days) AS average_delivery_days,
    SUM(
        CASE WHEN LOWER(CAST(is_delayed AS TEXT)) = 'true'
        THEN 1 ELSE 0 END
    ) AS delayed_orders
FROM orders_with_features
WHERE delivery_days IS NOT NULL
  AND delivery_delay_days IS NOT NULL;
"""
