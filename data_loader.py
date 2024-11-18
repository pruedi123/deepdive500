import pandas as pd

def load_bear_market_periods(filepath='bear_market_periods.xlsx'):
    """
    Loads bear market periods data from the specified Excel worksheet.
    """
    return pd.read_excel(filepath, sheet_name='bears')


def load_data(filepath='data.xlsx'):
    """
    Loads general market data from the specified Excel worksheet.
    """
    data = pd.read_excel(filepath, sheet_name='data')

    # Ensure column names are preserved as-is
    data.columns = data.columns.str.strip()
    print("Columns after loading from Excel:", data.columns.tolist())

    return data


def load_recession_data(filepath='recessions.xlsx'):
    """
    Loads recession data from the specified Excel worksheet.
    """
    return pd.read_excel(filepath, sheet_name='Sheet1')
