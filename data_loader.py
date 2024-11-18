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
    Loads general market data from the specified Excel worksheet and ensures the Date column is properly formatted.
    """
    # Load the Excel file
    try:
        data = pd.read_excel(filepath, sheet_name='data')
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{filepath}' was not found in the current directory.")
    except Exception as e:
        raise RuntimeError(f"Error loading data from '{filepath}': {e}")

    # Define the expected columns
    expected_columns = [
        "Date", "Composite", "Nominal Dividends", "Nominal Earnings",
        "CPI", "Total Return", "Real Earnings", "Real Composite",
        "Real Dividends", "Real Total Return"
    ]

    # Check for missing columns
    missing_columns = [col for col in expected_columns if col not in data.columns]
    if missing_columns:
        raise KeyError(f"The following columns are missing from the data: {missing_columns}")

    # Debug: Print column names for verification
    print("Loaded column names:", data.columns.tolist())
    st.write("Loaded column names:", data.columns.tolist())  # Debug info for Streamlit

    # Ensure the 'Date' column exists and is in the correct format
    if 'Date' not in data.columns:
        raise KeyError("The 'Date' column is missing.")
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce').dt.strftime('%Y-%m')

    # Drop rows where 'Date' could not be parsed
    data = data.dropna(subset=['Date'])

    return data
