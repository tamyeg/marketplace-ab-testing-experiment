-- PostgreSQL schema for generated, user-level, synthetic experiment data.
CREATE TABLE IF NOT EXISTS experiment_users (
    user_id BIGINT PRIMARY KEY,
    variant TEXT NOT NULL CHECK (variant IN ('control','treatment')),
    country TEXT NOT NULL,
    device TEXT NOT NULL,
    prior_buyer SMALLINT NOT NULL CHECK (prior_buyer IN (0,1)),
    clicked_listing SMALLINT NOT NULL CHECK (clicked_listing IN (0,1)),
    purchased_7d SMALLINT NOT NULL CHECK (purchased_7d IN (0,1)),
    order_value_eur NUMERIC(12,2) NOT NULL CHECK (order_value_eur >= 0),
    refunded_7d SMALLINT NOT NULL CHECK (refunded_7d IN (0,1))
);

-- Run in psql from repository root after generating CSV:
-- \copy experiment_users FROM 'data/experiment_users.csv' WITH (FORMAT csv, HEADER true)
