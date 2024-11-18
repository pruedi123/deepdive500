# ltc_bonds.py

import pandas as pd
import os
import sys

def load_data(excel_file='AAA_data_2.xlsx', sheet_name='ltc_bonds'):
    """
    Loads the financial data from the specified Excel file and sheet.

    Parameters:
        excel_file (str): Path to the Excel file.
        sheet_name (str): Name of the sheet/tab containing the data.

    Returns:
        pd.DataFrame: Processed financial data.

    Raises:
        FileNotFoundError: If the Excel file does not exist.
        ValueError: If required columns are missing or data is malformed.
    """
    if not os.path.exists(excel_file):
        raise FileNotFoundError(f"The specified Excel file '{excel_file}' was not found.")

    try:
        # Load the specified sheet from the Excel file
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        print(f"Successfully loaded '{sheet_name}' sheet from '{excel_file}'.")
    except ValueError as ve:
        raise ValueError(f"Error loading sheet '{sheet_name}': {ve}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while loading the Excel file: {e}")

    # Standardize column names: strip spaces, convert to lowercase, replace spaces with underscores
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    print("\nStandardized Columns:", df.columns.tolist())

    # Check for required columns
    required_columns = ['date', 'nominal_interest', 'nominal_total_return', 'real_interest', 'real_total_return']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"The following required columns are missing from the data: {missing_columns}")

    # Convert 'nominal_interest' from percentage string to float if necessary
    if df['nominal_interest'].dtype == object:
        # Handle percentage strings (e.g., '4.85%') or numeric strings (e.g., '0.05')
        df['nominal_interest'] = df['nominal_interest'].astype(str).str.rstrip('%').astype(float) / 100
        print("'nominal_interest' converted from percentage string to float.")

    # Convert 'real_interest' from percentage string to float if necessary
    if df['real_interest'].dtype == object:
        # Handle percentage strings (e.g., '4.85%') or numeric strings (e.g., '0.05')
        df['real_interest'] = df['real_interest'].astype(str).str.rstrip('%').astype(float) / 100
        print("'real_interest' converted from percentage string to float.")

    # Ensure 'nominal_total_return' is float
    if df['nominal_total_return'].dtype == object:
        df['nominal_total_return'] = pd.to_numeric(df['nominal_total_return'], errors='coerce')
        if df['nominal_total_return'].isnull().any():
            raise ValueError("Some 'nominal_total_return' values could not be converted to float.")

    # Ensure 'real_total_return' is float
    if df['real_total_return'].dtype == object:
        df['real_total_return'] = pd.to_numeric(df['real_total_return'], errors='coerce')
        if df['real_total_return'].isnull().any():
            raise ValueError("Some 'real_total_return' values could not be converted to float.")

    # Convert 'date' column to datetime in 'YYYY-MM' format
    df['date_dt'] = pd.to_datetime(df['date'], format='%Y-%m', errors='coerce')
    if df['date_dt'].isnull().any():
        raise ValueError("Some 'date' values could not be parsed. Ensure they are in 'YYYY-MM' format.")
    df['date'] = df['date_dt'].dt.strftime('%Y-%m')
    df.drop(columns=['date_dt'], inplace=True)

    # Drop rows with any NaN values in critical columns
    df.dropna(subset=['nominal_interest', 'nominal_total_return', 'real_interest', 'real_total_return', 'date'], inplace=True)

    # Display the processed DataFrame for verification
    print("\nProcessed DataFrame Head:")
    print(df.head())

    return df

def calculate_non_reinvesting_strategy(data_df, initial_investment):
    """
    Calculates metrics for the Non-Reinvesting Strategy for both Nominal and Real.

    Parameters:
        data_df (pd.DataFrame): Financial data containing 'nominal_interest', 'real_interest',
                                'nominal_total_return', and 'real_total_return'.
        initial_investment (float): The initial investment amount.

    Returns:
        dict: Metrics including total interest paid and ending value for both Nominal and Real strategies.
    """
    metrics = {}

    # Nominal Strategy
    data_df['nominal_interest_paid'] = data_df['nominal_interest'] * initial_investment
    total_nominal_interest = data_df['nominal_interest_paid'].sum()
    metrics['Total Interest Paid (Nominal)'] = total_nominal_interest
    metrics['Ending Value (Nominal)'] = initial_investment  # Should remain as initial investment

    # Real Strategy
    data_df['real_interest_paid'] = data_df['real_interest'] * initial_investment
    total_real_interest = data_df['real_interest_paid'].sum()
    metrics['Total Interest Paid (Real)'] = total_real_interest
    metrics['Ending Value (Real)'] = initial_investment  # Should remain as initial investment

    # Debugging Outputs
    print(f"Debug - Total Interest Paid (Nominal): ${metrics['Total Interest Paid (Nominal)']:.2f}")
    print(f"Debug - Ending Value (Nominal): ${metrics['Ending Value (Nominal)']:.2f}")
    print(f"Debug - Total Interest Paid (Real): ${metrics['Total Interest Paid (Real)']:.2f}")
    print(f"Debug - Ending Value (Real): ${metrics['Ending Value (Real)']:.2f}")

    return metrics

def calculate_reinvesting_strategy(data_df, initial_investment):
    """
    Calculates metrics for the Reinvesting Strategy for both Nominal and Real.

    Parameters:
        data_df (pd.DataFrame): Financial data containing 'nominal_total_return' and 'real_total_return'.
        initial_investment (float): The initial investment amount.

    Returns:
        dict: Metrics including relative return factor and ending value for both Nominal and Real strategies.
    """
    metrics = {}

    # Nominal Strategy
    if len(data_df) < 2:
        raise ValueError("Insufficient data to calculate nominal reinvestment strategy.")
    begin_nominal_total_return = data_df.iloc[0]['nominal_total_return']
    end_nominal_total_return = data_df.iloc[-1]['nominal_total_return']
    if begin_nominal_total_return == 0:
        raise ValueError("Begin 'nominal_total_return' is zero, cannot calculate relative return factor.")
    relative_return_nominal = end_nominal_total_return / begin_nominal_total_return
    ending_value_nominal = initial_investment * relative_return_nominal
    metrics['Relative Return Factor (Nominal)'] = relative_return_nominal
    metrics['Ending Value (Nominal)'] = ending_value_nominal

    # Real Strategy
    if len(data_df) < 2:
        raise ValueError("Insufficient data to calculate real reinvestment strategy.")
    begin_real_total_return = data_df.iloc[0]['real_total_return']
    end_real_total_return = data_df.iloc[-1]['real_total_return']
    if begin_real_total_return == 0:
        raise ValueError("Begin 'real_total_return' is zero, cannot calculate relative return factor.")
    relative_return_real = end_real_total_return / begin_real_total_return
    ending_value_real = initial_investment * relative_return_real
    metrics['Relative Return Factor (Real)'] = relative_return_real
    metrics['Ending Value (Real)'] = ending_value_real

    # Debugging Outputs
    print(f"Debug - Relative Return Factor (Nominal): {metrics['Relative Return Factor (Nominal)']:.2f}")
    print(f"Debug - Ending Value (Nominal): ${metrics['Ending Value (Nominal)']:.2f}")
    print(f"Debug - Relative Return Factor (Real): {metrics['Relative Return Factor (Real)']:.2f}")
    print(f"Debug - Ending Value (Real): ${metrics['Ending Value (Real)']:.2f}")

    return metrics

def main():
    # This module is intended to be imported, not run directly.
    pass

if __name__ == "__main__":
    main()