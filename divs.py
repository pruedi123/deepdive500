# divs.py
import pandas as pd
from data_loader import load_data
import graph  # Import the graph module for charting
import streamlit as st
import config  # Import config to access BEGIN_DATE and END_DATE constants

# November 15

# Nominal Dividend Calculations

def calculate_dividends_no_reinvestment(df, start_date=config.BEGIN_DATE, end_date=config.END_DATE, initial_investment=10000):
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m')
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)].reset_index(drop=True)
    results = {
        'Date': [], 'Composite Value': [], 'Dividend': [], 'Dividend %': [], 'Dividend Paid': [], 'Ending Value': []
    }
    ending_value = initial_investment
    total_dividends = 0

    for i in range(len(filtered_df)):
        date = filtered_df['Date'].iloc[i]
        composite_value = filtered_df['Composite'].iloc[i]
        dividend = filtered_df['Nominal Dividends'].iloc[i]
        dividend_percentage = (dividend / composite_value) / 12  # Monthly dividend %

        if i == 0:
            ending_value = initial_investment
        else:
            previous_composite_value = filtered_df['Composite'].iloc[i - 1]
            composite_return = composite_value / previous_composite_value
            ending_value *= composite_return

        dividend_paid = dividend_percentage * ending_value
        total_dividends += dividend_paid

        results['Date'].append(date)
        results['Composite Value'].append(composite_value)
        results['Dividend'].append(dividend)
        results['Dividend %'].append(dividend_percentage)
        results['Dividend Paid'].append(dividend_paid)
        results['Ending Value'].append(ending_value)

    final_ending_value = results['Ending Value'][-1]
    return pd.DataFrame(results), total_dividends, final_ending_value


def calculate_dividends_with_reinvestment(df, start_date=config.BEGIN_DATE, end_date=config.END_DATE, initial_investment=10000):
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m')
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)].reset_index(drop=True)
    results = {
        'Date': [], 'Total Return Value': [], 'Composite Value': [], 'Dividend': [], 'Dividend %': [],
        'Dividend Reinvested': [], 'Ending Value': []
    }
    ending_value = initial_investment
    total_dividends_reinvested = 0

    for i in range(len(filtered_df)):
        date = filtered_df['Date'].iloc[i]
        total_return_value = filtered_df['Total Return'].iloc[i]
        composite_value = filtered_df['Composite'].iloc[i]
        dividend = filtered_df['Nominal Dividends'].iloc[i]
        dividend_percentage = (dividend / composite_value) / 12

        if i > 0:
            previous_total_return_value = filtered_df['Total Return'].iloc[i - 1]
            total_return_growth = (total_return_value - previous_total_return_value) / previous_total_return_value
            ending_value *= (1 + total_return_growth)

        dividend_reinvested = dividend_percentage * ending_value
        total_dividends_reinvested += dividend_reinvested

        results['Date'].append(date)
        results['Total Return Value'].append(total_return_value)
        results['Composite Value'].append(composite_value)
        results['Dividend'].append(dividend)
        results['Dividend %'].append(dividend_percentage)
        results['Dividend Reinvested'].append(dividend_reinvested)
        results['Ending Value'].append(ending_value)

    final_ending_value = results['Ending Value'][-1]
    return pd.DataFrame(results), total_dividends_reinvested, final_ending_value


# Real Dividend Calculations

def calculate_real_dividends_no_reinvestment(df, start_date=config.BEGIN_DATE, end_date=config.END_DATE, initial_investment=10000):
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m')
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)].reset_index(drop=True)
    results = {
        'Date': [], 'Real Composite Value': [], 'Real Dividend': [], 'Dividend %': [], 'Dividend Paid': [], 'Real Ending Value': []
    }
    ending_value = initial_investment
    total_real_dividends = 0

    for i in range(len(filtered_df)):
        date = filtered_df['Date'].iloc[i]
        real_composite_value = filtered_df['Real Composite'].iloc[i]
        real_dividend = filtered_df['Real Dividends'].iloc[i]
        real_dividend_percentage = (real_dividend / real_composite_value) / 12

        if i > 0:
            previous_real_composite_value = filtered_df['Real Composite'].iloc[i - 1]
            real_composite_return = real_composite_value / previous_real_composite_value
            ending_value *= real_composite_return

        dividend_paid = real_dividend_percentage * ending_value
        total_real_dividends += dividend_paid

        results['Date'].append(date)
        results['Real Composite Value'].append(real_composite_value)
        results['Real Dividend'].append(real_dividend)
        results['Dividend %'].append(real_dividend_percentage)
        results['Dividend Paid'].append(dividend_paid)
        results['Real Ending Value'].append(ending_value)

    final_real_ending_value = results['Real Ending Value'][-1]
    return pd.DataFrame(results), total_real_dividends, final_real_ending_value


def calculate_real_dividends_with_reinvestment(df, start_date=config.BEGIN_DATE, end_date=config.END_DATE, initial_investment=10000):
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m')
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)].reset_index(drop=True)
    results = {
        'Date': [], 'Real Total Return Value': [], 'Real Composite Value': [], 'Real Dividend': [], 'Dividend %': [],
        'Dividend Reinvested': [], 'Real Ending Value': []
    }
    ending_value = initial_investment
    total_real_dividends_reinvested = 0

    for i in range(len(filtered_df)):
        date = filtered_df['Date'].iloc[i]
        real_total_return_value = filtered_df['Real Total Return'].iloc[i]
        real_composite_value = filtered_df['Real Composite'].iloc[i]
        real_dividend = filtered_df['Real Dividends'].iloc[i]
        real_dividend_percentage = (real_dividend / real_composite_value) / 12

        if i > 0:
            previous_real_total_return_value = filtered_df['Real Total Return'].iloc[i - 1]
            real_total_return_growth = (real_total_return_value - previous_real_total_return_value) / previous_real_total_return_value
            ending_value *= (1 + real_total_return_growth)

        dividend_reinvested = real_dividend_percentage * ending_value
        total_real_dividends_reinvested += dividend_reinvested

        results['Date'].append(date)
        results['Real Total Return Value'].append(real_total_return_value)
        results['Real Composite Value'].append(real_composite_value)
        results['Real Dividend'].append(real_dividend)
        results['Dividend %'].append(real_dividend_percentage)
        results['Dividend Reinvested'].append(dividend_reinvested)
        results['Real Ending Value'].append(ending_value)

    final_real_ending_value = results['Real Ending Value'][-1]
    return pd.DataFrame(results), total_real_dividends_reinvested, final_real_ending_value


# Wrapper Function to Calculate All Dividend Types

def calculate_dividends(df, start_date=config.BEGIN_DATE, end_date=config.END_DATE, initial_investment=10000):
    nominal_no_reinvestment_df, total_dividends_no_reinvestment, final_ending_value_no_reinvestment = calculate_dividends_no_reinvestment(
        df, start_date=start_date, end_date=end_date, initial_investment=initial_investment
    )

    nominal_with_reinvestment_df, total_dividends_reinvested, final_ending_value_reinvested = calculate_dividends_with_reinvestment(
        df, start_date=start_date, end_date=end_date, initial_investment=initial_investment
    )

    real_no_reinvestment_df, total_real_dividends_no_reinvestment, final_real_ending_value_no_reinvestment = calculate_real_dividends_no_reinvestment(
        df, start_date=start_date, end_date=end_date, initial_investment=initial_investment
    )

    real_with_reinvestment_df, total_real_dividends_reinvested, final_real_ending_value_reinvested = calculate_real_dividends_with_reinvestment(
        df, start_date=start_date, end_date=end_date, initial_investment=initial_investment
    )

    return {
        "Nominal_No_Reinvestment": (nominal_no_reinvestment_df, total_dividends_no_reinvestment, final_ending_value_no_reinvestment),
        "Nominal_With_Reinvestment": (nominal_with_reinvestment_df, total_dividends_reinvested, final_ending_value_reinvested),
        "Real_No_Reinvestment": (real_no_reinvestment_df, total_real_dividends_no_reinvestment, final_real_ending_value_no_reinvestment),
        "Real_With_Reinvestment": (real_with_reinvestment_df, total_real_dividends_reinvested, final_real_ending_value_reinvested),
    }


# Streamlit Display Code for Testing

if __name__ == "__main__":
    # Load the data
    try:
        data_df = load_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

    # Input for initial investment
    initial_investment = st.number_input("Initial Investment for Dividend Calculations", min_value=1000, value=10000)

    # Run the calculation
    dividend_results = calculate_dividends(data_df, start_date=config.BEGIN_DATE, end_date=config.END_DATE, initial_investment=initial_investment)

    # Display in Streamlit
    st.header("Dividend Calculations")

    for key, (df, total, final_value) in dividend_results.items():
        st.subheader(f"{key.replace('_', ' ')}")
        
        # Optionally display table data for each calculation
        st.write(f"**Total Dividends:** ${total:,.2f}")
        st.write(f"**Final Ending Value:** ${final_value:,.2f}")

        # Generate chart for each result
        chart_title = key.replace('_', ' ') + " - Dividends and Ending Value"
        fig = graph.create_dividends_ending_value_chart(df, title=chart_title)
        
        # Display the dataframe and plot in Streamlit
        # st.dataframe(df)  # Display the DataFrame
        st.plotly_chart(fig, use_container_width=True)