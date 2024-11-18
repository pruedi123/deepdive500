# data_loader.py
import pandas as pd
import streamlit as st
# November 15

def load_bear_market_periods(filepath='bear_market_periods.xlsx'):
    """
    Loads bear market periods data from the specified Excel worksheet.
    """
    return pd.read_excel(filepath, sheet_name='bears')


def load_data(filepath='data.xlsx'):
    """
    Loads general market data from the specified Excel worksheet and ensures the column names match expected format.
    """
    data = pd.read_excel(filepath, sheet_name='data')

    # Standardize column names if needed (optional)
    expected_columns = [
        "Date", "Composite", "Nominal Dividends", "Nominal Earnings", "CPI",
        "Total Return", "Real Earnings", "Real Composite", "Real Dividends", "Real Total Return"
    ]
    if not all(col in data.columns for col in expected_columns):
        raise KeyError(f"Expected columns: {expected_columns}, but got: {data.columns.tolist()}")

    return data


def load_recession_data(filepath='recessions.xlsx'):
    """
    Loads recession data from the specified Excel worksheet.
    """
    return pd.read_excel(filepath, sheet_name='Sheet1')



