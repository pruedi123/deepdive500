# bears.py

import pandas as pd
import streamlit as st
import config  # Import the config module for BEGIN_DATE and END_DATE
from data_loader import load_bear_market_periods
import plotly.express as px


def calculate_bear_market_metrics(bear_market_data, start_date, end_date, decline_threshold=-0.48):
    """
    Calculates various bear market metrics within a specified date range.

    Parameters:
    - bear_market_data (pd.DataFrame): DataFrame containing bear market periods and related metrics.
    - start_date (str or pd.Timestamp): The start date for filtering bear markets.
    - end_date (str or pd.Timestamp): The end date for filtering bear markets.
    - decline_threshold (float): The threshold for counting significant bear markets (default: -0.48 for -48%).

    Returns:
    - summary_table (pd.DataFrame): DataFrame summarizing bear market metrics.
    - filtered_bear_markets_display (pd.DataFrame): DataFrame of bear markets within the specified date range for display.
    """

    # Ensure the Date columns are properly formatted
    bear_market_data['Start Date'] = pd.to_datetime(
        bear_market_data['Bear Market Period'].str.split(' - ').str[0]
    )
    bear_market_data['End Date'] = pd.to_datetime(
        bear_market_data['Bear Market Period'].str.split(' - ').str[1]
    )

    # Validate date range
    if pd.to_datetime(end_date) < pd.to_datetime(start_date):
        st.error("End date must be after the start date.")
        return pd.DataFrame(), pd.DataFrame()

    # Filter bear markets within the date range
    filtered_bear_markets = bear_market_data[
        (bear_market_data['Start Date'] >= pd.to_datetime(start_date)) & 
        (bear_market_data['End Date'] <= pd.to_datetime(end_date))
    ]

    if filtered_bear_markets.empty:
        st.warning("No bear markets found within the selected date range.")
        return pd.DataFrame(), pd.DataFrame()

    # Ensure the 'Percentage Decline' column is numeric
    filtered_bear_markets['Percentage Decline'] = pd.to_numeric(
        filtered_bear_markets['Percentage Decline'], errors='coerce'
    ).fillna(0)

    # Sort the bear markets by 'Start Date' to ensure chronological order
    filtered_bear_markets = filtered_bear_markets.sort_values('Start Date').reset_index(drop=True)

    # Calculate the largest and average decline
    largest_decline = filtered_bear_markets['Percentage Decline'].min()
    average_decline = filtered_bear_markets['Percentage Decline'].mean()

    # Count bear markets worse than the specified threshold (default: -0.48 for -48%)
    num_bear_markets_worse_than_threshold = len(
        filtered_bear_markets[filtered_bear_markets['Percentage Decline'] <= decline_threshold]
    )

    # -----------------------------
    # Calculate Average Time Between Bear Markets (Start to Start)
    # -----------------------------

    # Compute the gap in days between the start dates of consecutive bear markets
    filtered_bear_markets['Gap Days Start to Start'] = filtered_bear_markets['Start Date'].diff().dt.days

    # Exclude the first bear market as it has no previous bear market to compare
    average_gap_days_start_to_start = filtered_bear_markets['Gap Days Start to Start'].iloc[1:].mean()

    # Handle cases where there might be no gaps (only one bear market)
    if pd.isna(average_gap_days_start_to_start):
        average_gap_days_start_to_start = 0

    # Convert average gap from days to years and months
    average_years_start = int(average_gap_days_start_to_start) // 365
    average_months_start = (int(average_gap_days_start_to_start) % 365) // 30

    # -----------------------------
    # Calculate Average Time Between End of One Bear Market to Start of Another
    # -----------------------------

    # Shift the 'End Date' down to align with the next bear market's 'Start Date'
    filtered_bear_markets['Previous End Date'] = filtered_bear_markets['End Date'].shift(1)

    # Calculate the gap in days between the previous end date and the current start date
    filtered_bear_markets['Gap Days End to Start'] = (
        filtered_bear_markets['Start Date'] - filtered_bear_markets['Previous End Date']
    ).dt.days

    # Exclude the first bear market as it has no previous bear market to compare
    average_gap_days_end_to_start = filtered_bear_markets['Gap Days End to Start'].iloc[1:].mean()

    # Handle cases where there might be no gaps (only one bear market)
    if pd.isna(average_gap_days_end_to_start):
        average_gap_days_end_to_start = 0

    # Convert average gap from days to years and months
    average_years_end = int(average_gap_days_end_to_start) // 365
    average_months_end = (int(average_gap_days_end_to_start) % 365) // 30

    # -----------------------------
    # Correct Formatting Before Creating Display DataFrame
    # -----------------------------

    # Correctly format the 'Percentage Decline' column by multiplying by 100
    filtered_bear_markets['Percentage Decline'] = filtered_bear_markets['Percentage Decline'].apply(
        lambda x: f"{x * 100:.1f}%"
    )

    # Format the 'Peak Value' and 'Trough Value' columns to two decimal places
    filtered_bear_markets['Peak Value'] = filtered_bear_markets['Peak Value'].apply(
        lambda x: f"{x:.2f}"
    )
    filtered_bear_markets['Trough Value'] = filtered_bear_markets['Trough Value'].apply(
        lambda x: f"{x:.2f}"
    )

    # -----------------------------
    # Create a Summary Table with Both Metrics
    # -----------------------------

    summary_table = pd.DataFrame({
        'Metric': [
            'Number of Bear Markets', 
            'Largest Decline (%)', 
            'Average Decline (%)', 
            'Average Time Between Bear Markets (Start to Start) (Years, Months)',
            'Average Time Between End of Bear Market to the Start of Another (Years, Months)',
            f'Bear Markets Worse Than {decline_threshold * 100}% Decline'
        ],
        'Value': [
            len(filtered_bear_markets), 
            f"{largest_decline * 100:.1f}%",  # Multiply by 100 to convert to percentage
            f"{average_decline * 100:.1f}%",  # Multiply by 100 to convert to percentage
            f"{average_years_start} years, {average_months_start} months", 
            f"{average_years_end} years, {average_months_end} months",
            num_bear_markets_worse_than_threshold
        ]
    })

    # -----------------------------
    # Prepare Display DataFrame
    # -----------------------------

    # Create a display DataFrame by dropping 'Start Date' and 'End Date'
    filtered_bear_markets_display = filtered_bear_markets.drop(columns=['Start Date', 'End Date', 'Gap Days Start to Start', 'Gap Days End to Start', 'Previous End Date'])

    return summary_table, filtered_bear_markets_display  # Return both summary and filtered data


def plot_decline_distribution(filtered_bear_markets):
    """
    Plots a histogram of bear market percentage declines.

    Parameters:
    - filtered_bear_markets (pd.DataFrame): DataFrame of bear markets within the specified date range.
    """
    # Extract numeric decline values by removing the '%' sign and converting to float
    decline_values = filtered_bear_markets['Percentage Decline'].str.rstrip('%').astype(float)

    fig = px.histogram(
        x=decline_values, 
        nbins=10, 
        title='Distribution of Bear Market Declines',
        labels={'x': 'Percentage Decline (%)', 'y': 'Count'},
        color_discrete_sequence=['indianred']
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_bear_market_timeline(filtered_bear_markets, bear_market_data, start_date, end_date):
    """
    Plots a timeline of bear markets.

    Parameters:
    - filtered_bear_markets (pd.DataFrame): DataFrame of bear markets within the specified date range.
    - bear_market_data (pd.DataFrame): Original bear market data for accurate date retrieval.
    - start_date (str or pd.Timestamp): The start date for filtering bear markets.
    - end_date (str or pd.Timestamp): The end date for filtering bear markets.
    """
    # Reconstruct 'Start Date' and 'End Date' from the original DataFrame
    bear_market_periods = bear_market_data[
        (bear_market_data['Start Date'] >= pd.to_datetime(start_date)) & 
        (bear_market_data['End Date'] <= pd.to_datetime(end_date))
    ].sort_values('Start Date').reset_index(drop=True)

    fig = px.timeline(
        bear_market_periods, 
        x_start="Start Date", 
        x_end="End Date", 
        y="Bear Market Period",
        title='Timeline of Bear Markets',
        labels={'Bear Market Period': 'Bear Market'}
    )
    fig.update_yaxes(autorange="reversed")  # Optional: To display the earliest periods at the top
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    # Load bear market data
    bear_market_data = load_bear_market_periods()
    
    # Use BEGIN_DATE and END_DATE from config for filtering
    start_date = config.BEGIN_DATE
    end_date = config.END_DATE
    
    # Add a slider for decline threshold
    decline_threshold = st.sidebar.slider(
        "Bear Market Decline Threshold (%)", 
        min_value=-100.0, 
        max_value=0.0, 
        value=-48.0, 
        step=0.1
    )
    # Convert threshold to decimal fraction
    decline_threshold_decimal = decline_threshold / 100

    # Calculate metrics with the user-defined threshold
    bear_metrics_summary, bear_filtered_data = calculate_bear_market_metrics(
        bear_market_data, 
        start_date, 
        end_date,
        decline_threshold=decline_threshold_decimal
    )

    # Display results in Streamlit
    st.write("Bear Market Summary Table")
    st.dataframe(bear_metrics_summary)

    st.write("Bear Markets During This Period")
    st.dataframe(bear_filtered_data)

    # Plotting
    st.write("Bear Market Decline Distribution")
    plot_decline_distribution(bear_filtered_data)

    st.write("Bear Market Timeline")
    plot_bear_market_timeline(bear_filtered_data, bear_market_data, start_date, end_date)