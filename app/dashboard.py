"""Streamlit dashboard for the news monitoring system.

This module defines a simple Streamlit application that reads records
from the SQLite database and displays them in an interactive table.  Users
can filter by source (Telegram or website) and search for keywords
within titles or content.

The app expects a ``config.yaml`` in the project root containing the
path to the database.  Running ``streamlit run app/dashboard.py``
will start the dashboard.
"""

import sqlite3
from typing import Any, Dict

import pandas as pd
import streamlit as st

from .config import load_config


def load_data(db_path: str) -> pd.DataFrame:
    """Read all messages from the SQLite database into a DataFrame.

    Parameters
    ----------
    db_path : str
        Path to the SQLite database file.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing all records, sorted by date descending.
    """
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(
        "SELECT id, source, channel, title, content, url, date FROM messages ORDER BY date DESC",
        conn,
    )
    conn.close()
    return df


def main() -> None:
    """Run the Streamlit dashboard application."""
    st.set_page_config(page_title="Iran HRS News Dashboard", layout="wide")
    st.title("Iran HRS News Monitoring Dashboard")

    # Load configuration
    try:
        config: Dict[str, Any] = load_config("config.yaml")
    except FileNotFoundError:
        st.error("Configuration file 'config.yaml' not found. Please create it from config_example.yaml.")
        return

    db_path = config.get("database", {}).get("path", "data/news.db")
    try:
        df = load_data(db_path)
    except Exception as exc:
        st.error(f"Unable to load data from database: {exc}")
        return

    if df.empty:
        st.info("No data available yet. Run the monitors to populate the database.")
        return

    # Filters
    source_options = df["source"].unique().tolist()
    selected_sources = st.multiselect("Filter by source", options=source_options, default=source_options)
    filtered_df = df[df["source"].isin(selected_sources)] if selected_sources else df

    search_term = st.text_input("Search text", "")
    if search_term:
        mask = (
            filtered_df["title"].str.contains(search_term, case=False, na=False)
            | filtered_df["content"].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[mask]

    # Display table
    st.dataframe(filtered_df, height=600)


if __name__ == "__main__":
    main()