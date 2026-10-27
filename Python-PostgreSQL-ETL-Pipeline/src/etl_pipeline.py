"""Demo ETL pipeline: CSV -> validation -> PostgreSQL + quarantine.

Uses synthetic data only. Configure DATABASE_URL before running.
Example:
    postgresql+psycopg2://user:password@localhost:5432/portfolio
"""

from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

SOURCE = Path(__file__).resolve().parents[1] / "data" / "sample_orders.csv"
DATABASE_URL = os.getenv("DATABASE_URL")

REQUIRED = ["order_id", "customer_id", "order_date", "amount"]


def utcnow():
    return datetime.now(timezone.utc)


def validate(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    data = df.copy()
    reasons = pd.Series("", index=data.index, dtype="string")

    duplicate_id = data["order_id"].duplicated(keep=False)
    reasons.loc[duplicate_id] += "duplicate order_id; "

    for col in REQUIRED:
        missing = data[col].isna() | data[col].astype("string").str.strip().eq("")
        reasons.loc[missing] += f"missing {col}; "

    parsed_dates = pd.to_datetime(data["order_date"], errors="coerce")
    invalid_date = parsed_dates.isna()
    reasons.loc[invalid_date] += "invalid order_date; "

    parsed_amount = pd.to_numeric(data["amount"], errors="coerce")
    invalid_amount = parsed_amount.isna() | parsed_amount.lt(0)
    reasons.loc[invalid_amount] += "invalid amount; "

    bad = reasons.ne("")
    rejected = data.loc[bad].copy()
    rejected["rejection_reason"] = reasons.loc[bad].str.rstrip("; ")

    valid = data.loc[~bad].copy()
    valid["order_date"] = parsed_dates.loc[~bad].dt.date
    valid["amount"] = parsed_amount.loc[~bad]
    valid["order_id"] = pd.to_numeric(valid["order_id"], errors="raise").astype("int64")

    return valid, rejected


def run() -> None:
    if not DATABASE_URL:
        raise RuntimeError("Set DATABASE_URL before running the pipeline.")

    engine = create_engine(DATABASE_URL)
    run_id = str(uuid.uuid4())
    started = utcnow()
    rows_read = rows_loaded = rows_rejected = 0

    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO portfolio_etl.etl_run_log
                (run_id, source_name, started_at, run_status)
                VALUES (:run_id, :source_name, :started_at, 'RUNNING')
            """),
            {"run_id": run_id, "source_name": SOURCE.name, "started_at": started},
        )

    try:
        raw = pd.read_csv(SOURCE)
        rows_read = len(raw)
        valid, rejected = validate(raw)
        rows_rejected = len(rejected)

        with engine.begin() as conn:
            if not rejected.empty:
                quarantine = rejected.astype("string")
                quarantine.insert(0, "run_id", run_id)
                quarantine.to_sql(
                    "orders_quarantine",
                    conn,
                    schema="portfolio_etl",
                    if_exists="append",
                    index=False,
                )

            for row in valid.to_dict("records"):
                conn.execute(
                    text("""
                        INSERT INTO portfolio_etl.orders_clean
                            (order_id, customer_id, order_date, amount, status)
                        VALUES
                            (:order_id, :customer_id, :order_date, :amount, :status)
                        ON CONFLICT (order_id) DO UPDATE SET
                            customer_id = EXCLUDED.customer_id,
                            order_date = EXCLUDED.order_date,
                            amount = EXCLUDED.amount,
                            status = EXCLUDED.status,
                            loaded_at = NOW()
                    """),
                    row,
                )
            rows_loaded = len(valid)

            conn.execute(
                text("""
                    UPDATE portfolio_etl.etl_run_log
                    SET finished_at = :finished_at,
                        rows_read = :rows_read,
                        rows_loaded = :rows_loaded,
                        rows_rejected = :rows_rejected,
                        run_status = 'SUCCESS'
                    WHERE run_id = :run_id
                """),
                {
                    "finished_at": utcnow(), "rows_read": rows_read,
                    "rows_loaded": rows_loaded, "rows_rejected": rows_rejected,
                    "run_id": run_id,
                },
            )

    except Exception as exc:
        with engine.begin() as conn:
            conn.execute(
                text("""
                    UPDATE portfolio_etl.etl_run_log
                    SET finished_at = :finished_at,
                        rows_read = :rows_read,
                        rows_loaded = :rows_loaded,
                        rows_rejected = :rows_rejected,
                        run_status = 'FAILED',
                        error_message = :error_message
                    WHERE run_id = :run_id
                """),
                {
                    "finished_at": utcnow(), "rows_read": rows_read,
                    "rows_loaded": rows_loaded, "rows_rejected": rows_rejected,
                    "error_message": str(exc)[:2000], "run_id": run_id,
                },
            )
        raise


if __name__ == "__main__":
    run()
