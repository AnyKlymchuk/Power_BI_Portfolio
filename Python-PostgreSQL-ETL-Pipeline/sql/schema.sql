CREATE SCHEMA IF NOT EXISTS portfolio_etl;

CREATE TABLE IF NOT EXISTS portfolio_etl.orders_clean (
    order_id        BIGINT PRIMARY KEY,
    customer_id     TEXT NOT NULL,
    order_date      DATE NOT NULL,
    amount          NUMERIC(14,2) NOT NULL CHECK (amount >= 0),
    status          TEXT,
    loaded_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS portfolio_etl.orders_quarantine (
    quarantine_id   BIGSERIAL PRIMARY KEY,
    run_id          UUID NOT NULL,
    order_id        TEXT,
    customer_id     TEXT,
    order_date      TEXT,
    amount          TEXT,
    status          TEXT,
    rejection_reason TEXT NOT NULL,
    quarantined_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS portfolio_etl.etl_run_log (
    run_id          UUID PRIMARY KEY,
    source_name     TEXT NOT NULL,
    started_at      TIMESTAMPTZ NOT NULL,
    finished_at     TIMESTAMPTZ,
    rows_read       INTEGER NOT NULL DEFAULT 0,
    rows_loaded     INTEGER NOT NULL DEFAULT 0,
    rows_rejected   INTEGER NOT NULL DEFAULT 0,
    run_status      TEXT NOT NULL CHECK (run_status IN ('RUNNING','SUCCESS','FAILED')),
    error_message   TEXT
);

CREATE INDEX IF NOT EXISTS ix_orders_clean_order_date
    ON portfolio_etl.orders_clean(order_date);

CREATE INDEX IF NOT EXISTS ix_quarantine_run_id
    ON portfolio_etl.orders_quarantine(run_id);
