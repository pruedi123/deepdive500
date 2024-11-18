import plotly.graph_objects as go
import pandas as pd

# November 15


# Existing function for creating dividend charts
def create_dividends_ending_value_chart(df, title="Dividends and Ending Value Over Time"):
    fig = go.Figure()

    if 'Dividend Paid' in df.columns:
        dividends_column = 'Dividend Paid'
    elif 'Dividend Reinvested' in df.columns:
        dividends_column = 'Dividend Reinvested'
    else:
        fig.update_layout(title="Error: No Dividend Data Found")
        return fig

    if 'Ending Value' in df.columns:
        ending_value_column = 'Ending Value'
    elif 'Real Ending Value' in df.columns:
        ending_value_column = 'Real Ending Value'
    else:
        fig.update_layout(title="Error: No Ending Value Data Found")
        return fig

    fig.add_trace(
        go.Scatter(
            x=df['Date'],
            y=df[dividends_column],
            name="Dividends",
            mode="lines",
            yaxis="y1"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df['Date'],
            y=df[ending_value_column],
            name="Ending Value",
            mode="lines",
            yaxis="y2"
        )
    )

    fig.update_layout(
        title=title,
        xaxis=dict(title="Date"),
        yaxis=dict(
            title="Dividends",
            titlefont=dict(color="blue"),
            tickfont=dict(color="blue")
        ),
        yaxis2=dict(
            title="Ending Value",
            titlefont=dict(color="green"),
            tickfont=dict(color="green"),
            anchor="x",
            overlaying="y",
            side="right"
        ),
        legend=dict(x=0.1, y=1.1, orientation="h")
    )

    return fig




def create_bar_chart(df, start_date, end_date, font_size=14):
    """
    Creates a bar chart for various increase factors over time.
    """
    import streamlit as st

    # Debugging: Verify DataFrame structure
    st.write("Columns in DataFrame passed to create_bar_chart:", df.columns.tolist())

    # Ensure column names match expected format
    required_columns = ['composite', 'nominal_dividends', 'nominal_earnings', 'cpi']
    if not all(col in df.columns for col in required_columns):
        raise KeyError(f"DataFrame must contain columns: {required_columns}")

    # Filter the DataFrame for the given date range
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    filtered_df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]

    # Debugging: Ensure filtered data exists
    st.write("Filtered DataFrame Preview:", filtered_df)

    if filtered_df.empty:
        raise ValueError(f"No data available between {start_date} and {end_date}")

    # Calculate increase factors
    composite_factor = filtered_df['composite'].iloc[-1] / filtered_df['composite'].iloc[0]
    earnings_factor = filtered_df['nominal_earnings'].iloc[-1] / filtered_df['nominal_earnings'].iloc[0]
    dividends_factor = filtered_df['nominal_dividends'].iloc[-1] / filtered_df['nominal_dividends'].iloc[0]
    cpi_factor = filtered_df['cpi'].iloc[-1] / filtered_df['cpi'].iloc[0]

    # Bar chart data
    factors = {
        "Composite": composite_factor,
        "Nominal Earnings": earnings_factor,
        "Nominal Dividends": dividends_factor,
        "CPI": cpi_factor,
    }

    # Create custom labels
    def format_label(value):
        if value > 1:
            return f"↑ {value:.1f}x"
        elif value < 1:
            return f"↓ {value:.1f}x"
        else:
            return f"↔ {value:.1f}x"

    custom_labels = [format_label(value) for value in factors.values()]

    # Create the bar chart
    fig = go.Figure(
        data=[
            go.Bar(
                x=list(factors.keys()),
                y=list(factors.values()),
                text=custom_labels,
                textposition='outside',
                marker=dict(color=["blue", "green", "orange", "red"]),
            )
        ]
    )

    fig.update_layout(
        title="Nothing Short of Miraculous",
        xaxis_title="Metric",
        yaxis_title="Increase Factor",
    )

    return fig
