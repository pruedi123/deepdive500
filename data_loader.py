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


import pandas as pd
import streamlit as st

def load_data(filepath='data.xlsx'):
    """
    Loads general market data from the specified Excel worksheet and ensures the date column is properly formatted.
    """
    data = pd.read_excel(filepath, sheet_name='data')
    
    # Standardize column names to lowercase
    data.columns = data.columns.str.strip().str.lower()

    # Ensure the 'date' column exists
    if 'date' not in data.columns:
        raise KeyError("The 'data' sheet must contain a 'date' column.")
    
    # Format the 'date' column to 'YYYY-MM'
    data['date'] = pd.to_datetime(data['date'], errors='coerce').dt.strftime('%Y-%m')
    
    # Drop rows where 'date' could not be parsed
    data = data.dropna(subset=['date'])

    return data
