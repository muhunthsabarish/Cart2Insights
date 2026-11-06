
import os
import sqlite3
from pathlib import Path

import pandas as pd


# Project directory (one level above streamlit/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Possible locations for project datasets
DATA_DIRS = [
    BASE_DIR / "data" / "cleaned",
    BASE_DIR
]


def find_dataset(filename):
    """Find a dataset in the cleaned-data or project-root folder."""
    for folder in DATA_DIRS:
        file_path = folder / filename
        if file_path.exists():
            return file_path

    raise FileNotFoundError(
        f"{filename} was not found. "
        "Check the data/cleaned folder and project root."
    )


def load_csv(filename):
    """Load a CSV dataset safely."""
    file_path = find_dataset(filename)
    return pd.read_csv(file_path)


def load_dashboard_data():
    """Load the three datasets required by the dashboard."""
    orders = load_csv("orders_with_features.csv")
    customers = load_csv("customer_features.csv")
    sellers = load_csv("seller_features.csv")

    return orders, customers, sellers


def load_reviews_data():
    """Load customer review data."""
    return load_csv("olist_order_reviews_dataset.csv")


def get_database_connection():
    """Connect to the project's SQLite database."""
    db_path = Path(
        os.getenv(
            "CART2INSIGHTS_DB",
            str(BASE_DIR / "data" / "cart2insights.db")
        )
    )

    db_path.parent.mkdir(parents=True, exist_ok=True)

    return sqlite3.connect(db_path)
