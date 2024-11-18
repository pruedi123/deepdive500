import pandas as pd

def load_data(filepath='data.xlsx'):
    """
    Loads general market data from the specified Excel worksheet and ensures the date column is properly formatted.
    """
    # Load the data from the Excel file
    data = pd.read_excel(filepath, sheet_name='data')

    # Debug: Print the column names
    print("Columns in the loaded data:", data.columns.tolist())
    
    # Ensure the date column exists
    if 'Date' not in data.columns:
        raise KeyError("The 'data' sheet must contain a 'Date' column.")

    # Format the 'Date' column to 'YYYY-MM'
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce').dt.strftime('%Y-%m')

    # Drop rows where 'Date' could not be parsed
    data = data.dropna(subset=['Date'])

    return data


def load_bear_market_periods(filepath='bear_market_periods.xlsx'):
    """
    Loads bear market periods data from the specified Excel worksheet.
    """
    return pd.read_excel(filepath, sheet_name='bears')


def load_recession_data(filepath='recessions.xlsx'):
    """
    Loads recession data from the specified Excel worksheet.
    """
    return pd.read_excel(filepath, sheet_name='Sheet1')
