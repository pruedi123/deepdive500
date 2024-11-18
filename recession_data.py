# recession_data.py
import pandas as pd
import streamlit as st
import config  # To access BEGIN_DATE and END_DATE constants
from data_loader import load_recession_data

# November 15


def calculate_recession_metrics(recession_data, start_date, end_date):
    # Convert dates to datetime format
    recession_data['Begin Date'] = pd.to_datetime(recession_data['Begin Date'])
    recession_data['End Date'] = pd.to_datetime(recession_data['End Date'])

    # Filter data for the given date range
    filtered_recessions = recession_data[
        (recession_data['Begin Date'] >= start_date) & 
        (recession_data['End Date'] <= end_date)
    ].reset_index(drop=True)

    # Calculate metrics
    num_recessions = len(filtered_recessions)
    worst_gdp_decline = filtered_recessions['Decline (%)'].min()
    average_frequency_days = filtered_recessions['Begin Date'].diff().mean().days
    peak_unemployment = filtered_recessions['Peak Unemployment (%)'].max()

    # Convert frequency from days to years and months
    average_years = average_frequency_days // 365
    average_months = (average_frequency_days % 365) // 30

    # Format metrics
    worst_gdp_decline_formatted = f"{worst_gdp_decline * 100:.1f}%"
    peak_unemployment_formatted = f"{peak_unemployment * 100:.1f}%"

    # Create summary table
    summary_table = pd.DataFrame({
        'Metric': [
            'Number of Recessions',
            'Worst GDP Decline (%)',
            'Average Frequency Between Recessions (Years, Months)',
            'Peak Unemployment (%)'
        ],
        'Value': [
            num_recessions,
            worst_gdp_decline_formatted,
            f"{average_years} years, {average_months} months",
            peak_unemployment_formatted
        ]
    })

    # Format Decline (%) and Peak Unemployment (%) columns
    filtered_recessions['Decline (%)'] = filtered_recessions['Decline (%)'] * 100
    filtered_recessions['Decline (%)'] = filtered_recessions['Decline (%)'].apply(lambda x: f"{x:.1f}%")

    filtered_recessions['Peak Unemployment (%)'] = filtered_recessions['Peak Unemployment (%)'] * 100
    filtered_recessions['Peak Unemployment (%)'] = filtered_recessions['Peak Unemployment (%)'].apply(lambda x: f"{x:.1f}%")

    # Format Begin Date and End Date to remove time component
    filtered_recessions['Begin Date'] = filtered_recessions['Begin Date'].dt.strftime('%Y-%m-%d')
    filtered_recessions['End Date'] = filtered_recessions['End Date'].dt.strftime('%Y-%m-%d')

    return summary_table, filtered_recessions

if __name__ == "__main__":
    # Load recession data
    recession_data = load_recession_data()

    # Use BEGIN_DATE and END_DATE from config for filtering
    start_date = config.BEGIN_DATE
    end_date = config.END_DATE

    # Calculate metrics
    recession_metrics_summary, recession_filtered_data = calculate_recession_metrics(recession_data, start_date, end_date)

    # Display results in Streamlit
    st.write("Recession Summary Table")
    st.dataframe(recession_metrics_summary)
    st.write("Recessions During This Period")
    st.dataframe(recession_filtered_data)
    