# data_loader.py
import pandas as pd

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

def load_market_data(filepath='data.xlsx'):
    try:
        data = pd.read_excel(filepath, sheet_name='data')
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{filepath}' was not found.")
    except Exception as e:
        raise RuntimeError(f"Error loading data from '{filepath}': {e}")

    # Standardize column names by stripping spaces (but keep original case)
    data.columns = data.columns.str.strip()

    # Ensure the 'Date' column exists
    if 'Date' not in data.columns:
        raise KeyError("The 'data' sheet must contain a 'Date' column.")

    # Convert 'Date' column to 'YYYY-MM'
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce').dt.strftime('%Y-%m')
    data = data.dropna(subset=['Date'])

    return data    