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




# Now we create the four metrics Bar Chart

import plotly.graph_objects as go

def create_bar_chart(df, start_date, end_date, font_size=14):
    """
    Creates a bar chart for various increase factors over time with bold customized labels and adjustable font size.

    Parameters:
    df (pd.DataFrame): DataFrame containing financial data.
    start_date (str): The start date for the range.
    end_date (str): The end date for the range.
    font_size (int): Font size for the bar labels.

    Returns:
    plotly.graph_objects.Figure: The generated bar chart.
    """
    import pandas as pd

    # Filter the DataFrame for the given date range
    df['Date'] = pd.to_datetime(df['Date'])
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    # Validate required columns
    required_columns = ['Composite', 'Nominal Earnings', 'Nominal Dividends', 'CPI']
    for col in required_columns:
        if col not in filtered_df.columns:
            raise KeyError(f"Missing column in DataFrame: {col}")

    # Calculate increase factors
    composite_factor = filtered_df['Composite'].iloc[-1] / filtered_df['Composite'].iloc[0]
    earnings_factor = filtered_df['Nominal Earnings'].iloc[-1] / filtered_df['Nominal Earnings'].iloc[0]
    dividends_factor = filtered_df['Nominal Dividends'].iloc[-1] / filtered_df['Nominal Dividends'].iloc[0]
    cpi_factor = filtered_df['CPI'].iloc[-1] / filtered_df['CPI'].iloc[0]

    # Bar chart data
    factors = {
        "Composite": composite_factor,
        "Nominal Earnings": earnings_factor,
        "Nominal Dividends": dividends_factor,
        "CPI": cpi_factor,
    }

    # Custom labels with arrows or placeholders, with bold formatting
    def format_label(value):
        if value > 1:
            return f"↑ {value:.2f}x"  # Up arrow for values greater than 1
        elif value < 1:
            return f"↓ {value:.2f}x"  # Down arrow for values less than 1
        else:
            return f"↔ {value:.2f}x"  # Neutral arrow for exactly 1

    # Apply custom labels
    custom_labels = [format_label(value) for value in factors.values()]

    # Create a bar chart
    fig = go.Figure(
        data=[
            go.Bar(
                x=list(factors.keys()),
                y=list(factors.values()),
                text=custom_labels,  # Use custom labels
                textposition='outside',  # Position labels outside the bars
                texttemplate=f'<b>%{{text}}</b>',  # Bold labels with Plotly formatting
                marker=dict(color=["blue", "green", "orange", "red"])  # Optional: color customization
            )
        ]
    )

    # Calculate y-axis range to fit bars and labels
    max_factor = max(factors.values())
    y_axis_range = [0, max_factor * 1.2]  # Add 20% headroom above the highest bar

    # Update layout with automargin and range adjustments
    fig.update_layout(
        title="Nothing Short of A Miracle ",
        xaxis_title="Metric",
        yaxis_title="Increase Factor",
        xaxis=dict(showgrid=False, automargin=True),  # Remove x-axis grid lines, enable automargin
        yaxis=dict(showgrid=False, range=y_axis_range, automargin=True),  # Remove y-axis grid lines, set range
        barmode="group",
        margin=dict(t=100, l=50, r=50, b=50),  # Ensure sufficient spacing
        legend_title="Metrics",
        font=dict(size=24)  # Set font size
    )

    return fig
    
