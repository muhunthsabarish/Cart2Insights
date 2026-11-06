-- ============================================================
-- Cart2Insights
-- Decoding E-Commerce Performance
-- SQL Business Analysis
-- Database: SQLite
-- ============================================================

-- 1. Total number of orders
SELECT
    COUNT(DISTINCT order_id) AS total_orders
FROM orders;

-- 2. Order status distribution
SELECT
    order_status,
    COUNT(*) AS order_count
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;

-- 3. Total revenue and average order value
SELECT
    ROUND(SUM(total_order_value), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(
        SUM(total_order_value) /
        NULLIF(COUNT(DISTINCT order_id), 0), 2
    ) AS average_order_value
FROM orders;

-- 4. Monthly sales analysis
SELECT
    strftime('%Y-%m', order_purchase_timestamp) AS sales_month,
    ROUND(SUM(total_order_value), 2) AS monthly_revenue,
    COUNT(DISTINCT order_id) AS total_orders
FROM orders
WHERE order_purchase_timestamp IS NOT NULL
GROUP BY sales_month
ORDER BY sales_month;

-- 5. Top 10 customers by spending
SELECT
    customer_unique_id,
    total_orders,
    ROUND(total_spending, 2) AS total_spending,
    ROUND(customer_aov, 2) AS average_order_value
FROM customer_features
ORDER BY total_spending DESC
LIMIT 10;

-- 6. Repeat customer analysis
SELECT
    is_repeat_customer,
    COUNT(*) AS customer_count
FROM customer_features
GROUP BY is_repeat_customer;

-- 7. Top 10 sellers by revenue
SELECT
    seller_id,
    order_count,
    item_count,
    ROUND(seller_revenue, 2) AS seller_revenue
FROM seller_features
ORDER BY seller_revenue DESC
LIMIT 10;

-- 8. Delivery performance
SELECT
    order_status,
    COUNT(*) AS order_count,
    ROUND(AVG(delivery_days), 2) AS average_delivery_days,
    ROUND(AVG(delivery_delay_days), 2) AS average_delay_days
FROM orders
WHERE delivery_days IS NOT NULL
GROUP BY order_status
ORDER BY average_delivery_days;

-- 9. Orders with delayed delivery
SELECT
    COUNT(*) AS delayed_orders
FROM orders
WHERE LOWER(CAST(is_delayed AS TEXT)) = 'true';

-- 10. Customers with spending above average
SELECT
    customer_unique_id,
    total_spending
FROM customer_features
WHERE total_spending > (
    SELECT AVG(total_spending)
    FROM customer_features
)
ORDER BY total_spending DESC;

-- 11. Customer ranking using a window function
SELECT
    customer_unique_id,
    total_spending,
    RANK() OVER (
        ORDER BY total_spending DESC
    ) AS spending_rank
FROM customer_features
LIMIT 20;

-- 12. Seller revenue ranking using CTE
WITH seller_ranking AS (
    SELECT
        seller_id,
        seller_revenue,
        RANK() OVER (
            ORDER BY seller_revenue DESC
        ) AS revenue_rank
    FROM seller_features
)
SELECT *
FROM seller_ranking
WHERE revenue_rank <= 10
ORDER BY revenue_rank;
