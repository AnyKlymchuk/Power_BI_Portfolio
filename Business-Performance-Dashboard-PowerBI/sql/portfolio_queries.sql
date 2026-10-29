-- Business Performance Dashboard | SQL examples

-- 1. Monthly sales performance
SELECT
    DATE_TRUNC('month', order_date) AS month,
    SUM(revenue) AS revenue,
    SUM(profit) AS profit,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(profit) / NULLIF(SUM(revenue), 0) * 100, 2) AS profit_margin_pct
FROM fact_sales
WHERE status <> 'Cancelled'
GROUP BY 1
ORDER BY 1;

-- 2. Performance by region
SELECT
    region,
    SUM(revenue) AS revenue,
    SUM(profit) AS profit,
    COUNT(DISTINCT order_id) AS orders
FROM fact_sales
WHERE status <> 'Cancelled'
GROUP BY region
ORDER BY revenue DESC;

-- 3. Top customers
SELECT
    customer_name,
    industry,
    segment,
    SUM(revenue) AS revenue,
    SUM(profit) AS profit
FROM fact_sales
WHERE status <> 'Cancelled'
GROUP BY customer_name, industry, segment
ORDER BY revenue DESC
LIMIT 10;
