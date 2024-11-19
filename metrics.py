import pandas as pd
import streamlit as st
from data_loader import load_data

# November 16

def calculate_metrics(df, start_date, end_date, initial_investment=10000, decimals=2):
    """
    Calculates the beginning value, ending value, and increase factor for each column except Date Fraction and Date.
    Uses initial investment for Total Return and Real Total Return calculations.

    Parameters:
    df (pd.DataFrame): The data containing financial metrics.
    start_date (str): The starting date in 'YYYY-MM' format.
    end_date (str): The ending date in 'YYYY-MM' format.
    initial_investment (float): The initial investment value for Total Return and Real Total Return.
    decimals (int): Number of decimal places to display for non-currency values.

    Returns:
    pd.DataFrame: A DataFrame with calculated metrics.
    """
    # Set decimal format string
    decimal_format = f"{{:.{decimals}f}}"
    
    # Convert the Date column to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m')
    # Filter the DataFrame for the specified date range
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    
    # Define columns to include, excluding Date and Date Fraction
    columns_to_include = [col for col in df.columns if col not in ['Date', 'Date Fraction']]

    # Initialize an empty dictionary to store metrics
    metrics = {
        'Metric': [],
        'Begin Value': [],
        'End Value': [],
        'Increase Factor': []
    }
    
    # Calculate metrics for each numeric column
    for column in columns_to_include:
        begin_value = filtered_df[column].iloc[0]
        end_value = filtered_df[column].iloc[-1]

        # Special handling for Total Return and Real Total Return
        if column in ['Total Return', 'Real Total Return']:
            begin_value = initial_investment
            increase_factor = end_value / filtered_df[column].iloc[0]
            end_value = begin_value * increase_factor

            # Format begin and end values as currency with no decimals
            begin_value = f"${begin_value:,.0f}"
            end_value = f"${end_value:,.0f}"
            # Apply decimal format for Increase Factor
            increase_factor = decimal_format.format(increase_factor)
        else:
            increase_factor = end_value / begin_value

            # Apply decimal formatting for other values
            begin_value = decimal_format.format(begin_value)
            end_value = decimal_format.format(end_value)
            increase_factor = decimal_format.format(increase_factor)

        # Append results to the metrics dictionary
        metrics['Metric'].append(column)
        metrics['Begin Value'].append(begin_value)
        metrics['End Value'].append(end_value)
        metrics['Increase Factor'].append(increase_factor)

    return pd.DataFrame(metrics)


def calculate_comparison_table(bond_results, dividend_results, initial_investment):
    """
    Prepares a DataFrame with bond and dividend comparison metrics.

    Parameters:
    bond_results (tuple): Results from calculate_investment_yields (non-reinvested and reinvested DataFrames).
    dividend_results (dict): Results from calculate_dividends.
    initial_investment (float): Initial investment amount.

    Returns:
    pd.DataFrame: DataFrame with formatted comparison data.
    """
    non_reinvested_df, reinvested_df = bond_results

    # Calculate bond metrics
    total_cumulative_interest_non_reinvested = round(non_reinvested_df['Interest_Payment'].sum())
    total_cumulative_interest_reinvested = round(reinvested_df['Cumulative_Interest'].iloc[-1])
    ending_value_non_reinvested = round(initial_investment + total_cumulative_interest_non_reinvested)
    ending_value_reinvested = round(reinvested_df['Ending_Value'].iloc[-1])

    # Extract dividend metrics
    nominal_dividend_non_reinvested = round(dividend_results["Nominal_No_Reinvestment"][1])
    final_nominal_value_non_reinvested = round(dividend_results["Nominal_No_Reinvestment"][2])

    nominal_dividend_reinvested = round(dividend_results["Nominal_With_Reinvestment"][1])
    final_nominal_value_reinvested = round(dividend_results["Nominal_With_Reinvestment"][2])

    # Prepare comparison table
    comparison_table_data = {
        "Strategy": [
            "Nominal SP500 Investment--No Reinvestment",
            "Nominal Bonds Investment--No Reinvestment",
            "Nominal SP500 Investment--With Reinvestment",
            "Nominal Bonds Investment--With Reinvestment",
        ],
        "Total Dividends/Interest": [
            f"${nominal_dividend_non_reinvested:,}",
            f"${total_cumulative_interest_non_reinvested:,}",
            f"${nominal_dividend_reinvested:,}",
            f"${total_cumulative_interest_reinvested:,}",
        ],
        "Ending Value": [
            f"${final_nominal_value_non_reinvested:,}",
            f"${ending_value_non_reinvested:,}",
            f"${final_nominal_value_reinvested:,}",
            f"${ending_value_reinvested:,}",
        ],
    }

    return pd.DataFrame(comparison_table_data)


def calculate_periods_metrics(data_df, predefined_periods, end_date, initial_investment=10000):
    """
    Calculates metrics for predefined periods ending at a specific date.

    Parameters:
    data_df (pd.DataFrame): The data containing financial metrics.
    predefined_periods (list): List of predefined periods in years.
    end_date (str): The ending date in 'YYYY-MM' format.
    initial_investment (float): Initial investment value for Total Return and Real Total Return.

    Returns:
    dict: A dictionary of DataFrames for each predefined period.
    """
    # Convert the Date column to datetime format
    data_df['Date'] = pd.to_datetime(data_df['Date'], format='%Y-%m')

    # Convert end_date to datetime
    end_date = pd.to_datetime(end_date)

    # Prepare results for each predefined period
    results = {}
    for years in predefined_periods:
        start_date = end_date - pd.DateOffset(years=years)
        filtered_df = data_df[(data_df['Date'] >= start_date) & (data_df['Date'] <= end_date)]

        # Calculate metrics for this period
        metrics_df = calculate_metrics(filtered_df, start_date=start_date, end_date=end_date, initial_investment=initial_investment)
        results[f"Last {years} Years"] = metrics_df

    return results


# Streamlit Testing Code
if __name__ == "__main__":
    # Define default start and end dates
    BEGIN_DATE = '1959-10'
    END_DATE = '2024-09'

    # Load the data
    data_df = load_data()

    # Input for initial investment
    initial_investment = st.number_input("Initial Investment for Total Return Calculations", min_value=1000, value=10000)
    
    # Input for number of decimals
    decimals = st.number_input("Number of Decimals for Non-Currency Values", min_value=0, max_value=5, value=2)

    # Calculate metrics and display them
    metrics_df = calculate_metrics(data_df, start_date=BEGIN_DATE, end_date=END_DATE, initial_investment=initial_investment, decimals=decimals)
    st.write("Financial Metrics for Specified Period")
    st.dataframe(metrics_df)

    # Testing predefined periods
    predefined_periods = [1, 3, 5, 10, 15, 20, 25, 30, 35, 40, 50]
    periods_metrics = calculate_periods_metrics(data_df, predefined_periods, end_date=END_DATE, initial_investment=initial_investment)

    for period, df in periods_metrics.items():
        st.write(f"Metrics for {period}")
        st.dataframe(df)

    # Testing the comparison table
    # Simulate bond and dividend data for testing
    mock_bond_results = (pd.DataFrame(), pd.DataFrame())  # Replace with actual bond results
    mock_dividend_results = {
        "Nominal_No_Reinvestment": ("", 1000, 2000),
        "Nominal_With_Reinvestment": ("", 1500, 3000)
    }

    comparison_table = calculate_comparison_table(mock_bond_results, mock_dividend_results, initial_investment)
    st.write("Bond and Dividend Comparison Table")
    st.dataframe(comparison_table)
    