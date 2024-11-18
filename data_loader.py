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
    Loads general market data from the specified Excel worksheet.
    """
    return pd.read_excel(filepath, sheet_name='data')


def load_recession_data(filepath='recessions.xlsx'):
    """
    Loads recession data from the specified Excel worksheet.
    """
    return pd.read_excel(filepath, sheet_name='Sheet1')


def load_data(filepath='data.xlsx'):
    """
    Loads general market data from the specified Excel worksheet and ensures column names are standardized.
    """
    data = pd.read_excel(filepath, sheet_name='data')
    data.columns = (
        data.columns
        .str.strip()        # Remove extra spaces
        .str.lower()        # Convert to lowercase
        .str.replace(' ', '_')  # Replace spaces with underscores
    )

    # Ensure 'date' exists and is properly formatted
    if 'date' not in data.columns:
        raise KeyError("The 'data' sheet must contain a 'date' column.")
    data['date'] = pd.to_datetime(data['date'], errors='coerce')

    return data
