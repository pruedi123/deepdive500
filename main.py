# main.py

import streamlit as st
from data_loader import load_data, load_bear_market_periods, load_recession_data
from bears import calculate_bear_market_metrics
from recession_data import calculate_recession_metrics
from divs import calculate_dividends
from ltc_bonds import load_data as load_bond_data, calculate_non_reinvesting_strategy, calculate_reinvesting_strategy
import graph
from utility import format_table
from metrics import calculate_metrics, calculate_comparison_table
from investment_comparison import create_comparison_table
import pandas as pd
import numpy as np



# Define the default end date
DEFAULT_END_DATE = "2024-09"

# Sidebar for user inputs
st.sidebar.header("Inputs")

# Generate date options for dropdowns
date_options = [
    f"{year}-{month:02}" for year in range(1875, 2025)
    for month in range(1, 13)
    if not (year == 2024 and month > 9)
]

# Checkbox to choose between custom dates or predefined periods
custom_date_mode = st.sidebar.checkbox("Use Custom Begin and End Dates", value=False)

if custom_date_mode:
    # If custom mode, allow date selection
    try:
        begin_date = st.sidebar.selectbox("Select Begin Date", date_options, index=date_options.index("1959-09"))
    except ValueError:
        begin_date = "1959-09"  # Fallback in case "1959-09" is not in date_options
    try:
        end_date = st.sidebar.selectbox("Select End Date", date_options, index=date_options.index(DEFAULT_END_DATE))
    except ValueError:
        end_date = DEFAULT_END_DATE  # Fallback if default end date not found
else:
    # If not custom, use predefined periods
    predefined_periods_dict = {
        "Last 1 Year": 1,
        "Last 3 Years": 3,
        "Last 5 Years": 5,
        "Last 10 Years": 10,
        "Last 15 Years": 15,
        "Last 20 Years": 20,
        "Last 25 Years": 25,
        "Last 30 Years": 30,
        "Last 35 Years": 35,
        "Last 40 Years": 40,
        "Last 50 Years": 50,
        "Last 60 Years": 60,
        "Last 70 Years": 70,
        "Last 80 Years": 80,
        "Last 90 Years": 90,
        "Enf of WW2": "1945-09",
    }

    # Set default selected period to "Last 30 Years"
    try:
        selected_period_label = st.sidebar.selectbox(
            "Select Predefined Period",
            list(predefined_periods_dict.keys()),
            index=list(predefined_periods_dict.keys()).index("Last 30 Years")  # Set default to "Last 30 Years"
        )
    except ValueError:
        selected_period_label = "Last 30 Years"  # Fallback if "Last 30 Years" not found

    try:
        end_date = st.sidebar.selectbox("Select End Date", date_options, index=date_options.index(DEFAULT_END_DATE))
    except ValueError:
        end_date = DEFAULT_END_DATE  # Fallback if default end date not found

    end_date_dt = pd.to_datetime(end_date)

    if selected_period_label == "WW2":
        begin_date = "1945-09"  # Set the specific begin date for WW2
    else:
        # Calculate the begin date for other predefined periods
        years_offset = predefined_periods_dict[selected_period_label]
        begin_date_dt = end_date_dt - pd.DateOffset(years=years_offset)
        begin_date = begin_date_dt.strftime("%Y-%m")

# Input box for Initial Investment
initial_investment = st.sidebar.number_input(
    "Initial Investment for Calculations",
    min_value=1000,
    max_value=1000000,
    value=10000,
    step=10000
)

# Cache loaded data to avoid redundant reloads
@st.cache_data
def get_data():
    return {
        "data_df": load_data(),
        "bear_market_data": load_bear_market_periods(),
        "recession_data": load_recession_data(),
    }

data = get_data()

# Cache loaded bond data to avoid redundant reloads
@st.cache_data
def get_bond_data():
    return load_bond_data(excel_file='AAA_data_2.xlsx', sheet_name='ltc_bonds')

# Load bond data
bond_data = get_bond_data()

# Ensure 'date' is in datetime format for filtering
bond_data['date_dt'] = pd.to_datetime(bond_data['date'], format='%Y-%m', errors='coerce')

# Filter bond data based on user-selected date range
bond_mask = (bond_data['date_dt'] >= pd.to_datetime(begin_date, format='%Y-%m')) & (bond_data['date_dt'] <= pd.to_datetime(end_date, format='%Y-%m'))
bond_filtered_data = bond_data.loc[bond_mask].sort_values('date_dt').copy()

if bond_filtered_data.empty:
    st.warning("No bond data available for the selected date range.")
else:
    # Drop the temporary 'date_dt' column
    bond_filtered_data.drop(columns=['date_dt'], inplace=True)

# Utility to display tables with proper formatting
def display_table(title, dataframe):
    st.write(title)
    st.table(format_table(dataframe))

# Calculate and display Bear Market Metrics
bear_metrics_summary, bear_filtered_data = calculate_bear_market_metrics(
    data["bear_market_data"], start_date=begin_date, end_date=end_date
)
display_table("Bear Market Summary Table", bear_metrics_summary)

# Calculate and display Recession Metrics
recession_metrics_summary, recession_filtered_data = calculate_recession_metrics(
    data["recession_data"], start_date=begin_date, end_date=end_date
)
display_table("Recession Summary Table", recession_metrics_summary)

# Add the new bar chart after the Recession Summary Table
st.header("What did The Managers of The Great Companies of America Produce in the Face of Such Trauma...")
bar_chart_fig = graph.create_bar_chart(
    data["data_df"], 
    start_date=begin_date, 
    end_date=end_date
)
st.plotly_chart(bar_chart_fig, use_container_width=True)

# Add checkboxes for optional display of Nominal and Real Dividends
st.header("A Deeper Dive Into Data")
show_nominal = st.checkbox("Show Nominal Dividend Charts")
show_real = st.checkbox("Show Real Dividend Charts")

# Calculate dividends
dividend_results = calculate_dividends(
    data["data_df"], start_date=begin_date, end_date=end_date, initial_investment=initial_investment
)

for key, (df, total, final_value) in dividend_results.items():
    if "With_Reinvestment" in key:
        # Reinvested strategies
        if ("Nominal" in key and show_nominal) or ("Real" in key and show_real):
            st.subheader(f"{key.replace('_', ' ')}")
            # st.write("**Total Dividends/Interest:** NA")
            st.write(f"**Final Ending Value:** ${final_value:,.2f}")

            # Create and display charts
            chart_title = key.replace('_', ' ') + " - Dividends and Ending Value"
            fig = graph.create_dividends_ending_value_chart(df, title=chart_title)
            st.plotly_chart(fig, use_container_width=True)
    else:
        # Non-reinvested strategies
        if ("Nominal" in key and show_nominal) or ("Real" in key and show_real):
            st.subheader(f"{key.replace('_', ' ')}")
            st.write(f"**Total Dividends/Interest:** ${total:,.2f}")
            st.write(f"**Final Ending Value:** ${final_value:,.2f}")

            # Create and display charts
            chart_title = key.replace('_', ' ') + " - Dividends and Ending Value"
            fig = graph.create_dividends_ending_value_chart(df, title=chart_title)
            st.plotly_chart(fig, use_container_width=True)

# Additional Financial Metrics
if st.checkbox("Show Additional Financial Metrics"):
    try:
        metrics_df = calculate_metrics(
            data["data_df"], 
            start_date=begin_date, 
            end_date=end_date, 
            initial_investment=initial_investment, 
            decimals=0
        )
        display_table("Additional Financial Metrics During This Period", metrics_df)
    except Exception as e:
        st.error(f"Error calculating metrics: {e}")

# Display Bear Markets and Recessions During the Period
if st.checkbox("Show Bear Markets During This Period"):
    display_table("Bear Markets During This Period", bear_filtered_data)

if st.checkbox("Show Recessions During This Period"):
    display_table("Recessions During This Period", recession_filtered_data)

# Display Bond Results
try:
    cpi_data = data["data_df"]  # Assuming the CPI data is loaded in the 'data_df'

    # Generate Nominal and Real comparison tables
    nominal_table = create_comparison_table(
        sp500_data=data["data_df"],
        bond_data=bond_filtered_data,
        initial_investment=initial_investment,
        begin_date=begin_date,
        end_date=end_date,
        data_type="Nominal",
    )

    real_table = create_comparison_table(
        sp500_data=data["data_df"],
        bond_data=bond_filtered_data,
        initial_investment=initial_investment,
        begin_date=begin_date,
        end_date=end_date,
        data_type="Real",
        cpi_data=cpi_data,  # Pass the CPI data
    )
    # Checkbox to control the display of both tables
    show_tables = st.checkbox("Show Nominal and Real Comparison Tables")

    if show_tables:
        # Format and display the Nominal Comparison Table
        st.subheader("Comparison of Nominal Investments")
        formatted_nominal_table = format_table(nominal_table)
        st.table(formatted_nominal_table)

        # Format and display the Real Comparison Table
        st.subheader("Comparison of Real Investments")
        formatted_real_table = format_table(real_table)
        st.table(formatted_real_table)

except Exception as e:
    st.error(f"Error displaying the comparison tables: {e}")
