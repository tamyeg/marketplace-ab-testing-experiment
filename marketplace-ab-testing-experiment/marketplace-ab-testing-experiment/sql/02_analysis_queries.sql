-- 1. Randomized user counts and key outcomes by assigned variant.
SELECT variant, COUNT(*) AS users, SUM(purchased_7d) AS purchases,
       ROUND(AVG(purchased_7d::numeric) * 100, 3) AS purchase_conversion_pct,
       ROUND(AVG(clicked_listing::numeric) * 100, 3) AS listing_click_pct,
       ROUND(AVG(order_value_eur), 2) AS gross_value_per_user_eur
FROM experiment_users GROUP BY variant ORDER BY variant;

-- 2. Sample ratio mismatch diagnostic against a planned 50/50 split.
SELECT variant, COUNT(*) AS assigned_users,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS assigned_pct
FROM experiment_users GROUP BY variant ORDER BY variant;

-- 3. Balance check on a PRE-treatment user attribute.
SELECT variant, COUNT(*) AS users,
       ROUND(AVG(prior_buyer::numeric) * 100, 2) AS prior_buyer_pct
FROM experiment_users GROUP BY variant ORDER BY variant;

-- 4. Exploratory segmentation: not a pre-registered primary hypothesis test.
SELECT country, variant, COUNT(*) AS users,
       ROUND(100.0 * AVG(purchased_7d::numeric), 3) AS purchase_conversion_pct
FROM experiment_users GROUP BY country, variant ORDER BY country, variant;

-- 5. Descriptive guardrail among purchasers (selected post-treatment group).
SELECT variant, SUM(purchased_7d) AS purchasers,
       SUM(refunded_7d) AS refunded_orders,
       ROUND(100.0 * SUM(refunded_7d) / NULLIF(SUM(purchased_7d), 0), 2) AS refunds_per_purchaser_pct
FROM experiment_users GROUP BY variant ORDER BY variant;
