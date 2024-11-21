import pandas as pd
from investment_comparison import create_comparison_table
from utility import format_table  # Ensure this utility is available

def calculate_income_metrics(data_df, bond_filtered_data, initial_investment, begin_date, end_date):
    try:
        # Ensure Date column is in datetime format
        data_df["Date"] = pd.to_datetime(data_df["Date"], format='%Y-%m', errors='coerce')
        ending_month = pd.to_datetime(end_date, format='%Y-%m')

        # Find the closest available date in the data
        available_dates = data_df["Date"].dropna()
        nearest_date = available_dates[available_dates <= ending_month].max()

        if pd.isna(nearest_date):
            raise ValueError(f"No data available for or before the selected end date: {end_date}")

        # Create the nominal comparison table
        nominal_table = create_comparison_table(
            sp500_data=data_df,
            bond_data=bond_filtered_data,
            initial_investment=initial_investment,
            begin_date=begin_date,
            end_date=end_date,
            data_type="Nominal",
        )

        # Adjust index if necessary
        if "Strategy" in nominal_table.columns:
            nominal_table.set_index("Strategy", inplace=True)

        # Convert "Ending Value" to numeric
        nominal_table["Ending Value"] = nominal_table["Ending Value"].replace('[\$,]', '', regex=True).astype(float)

        # Calculate dividend rate for SPX
        dividend_rate = (
            data_df.loc[data_df["Date"] == nearest_date, "Nominal Dividends"].values[0] /
            data_df.loc[data_df["Date"] == nearest_date, "Composite"].values[0]
        )

        # Calculate Current Income for SPX
        spx_current_income_no_reinvestment = (
            dividend_rate * nominal_table.loc["Nominal SP500 Investment–No Reinvestment", "Ending Value"]
        )
        spx_current_income_with_reinvestment = (
            dividend_rate * nominal_table.loc["Nominal SP500 Investment–With Reinvestment", "Ending Value"]
        )

        # Get the last nominal_interest value for Long Term Bonds
        nominal_interest_rate = bond_filtered_data["nominal_interest"].iloc[-1]
        ltc_current_income_no_reinvestment = (
            nominal_interest_rate * nominal_table.loc["Nominal Bonds Investment–No Reinvestment", "Ending Value"]
        )
        ltc_current_income_with_reinvestment = (
            nominal_interest_rate * nominal_table.loc["Nominal Bonds Investment–With Reinvestment", "Ending Value"]
        )

        # Create DataFrame for the table with custom row order
        income_metrics_df = pd.DataFrame({
            "Category": [
                "Nominal SP500 Investment–No Reinvestment",
                "Nominal Bonds Investment–No Reinvestment",
                "Nominal SP500 Investment–With Reinvestment",
                "Nominal Bonds Investment–With Reinvestment",
            ],
            "Initial Value": [initial_investment] * 4,  # Add the same value for all categories
            "Ending Value": [
                nominal_table.loc["Nominal SP500 Investment–No Reinvestment", "Ending Value"],
                nominal_table.loc["Nominal Bonds Investment–No Reinvestment", "Ending Value"],
                nominal_table.loc["Nominal SP500 Investment–With Reinvestment", "Ending Value"],
                nominal_table.loc["Nominal Bonds Investment–With Reinvestment", "Ending Value"],
            ],
            "Current Income": [
                spx_current_income_no_reinvestment,
                ltc_current_income_no_reinvestment,
                spx_current_income_with_reinvestment,
                ltc_current_income_with_reinvestment,
            ],
            "Current Income as % of Original Investment": [
                (spx_current_income_no_reinvestment / initial_investment) * 100,
                (ltc_current_income_no_reinvestment / initial_investment) * 100,
                (spx_current_income_with_reinvestment / initial_investment) * 100,
                (ltc_current_income_with_reinvestment / initial_investment) * 100,
            ],
        })

        # Apply formatting to the table
        income_metrics_df["Initial Value"] = income_metrics_df["Initial Value"].map("${:,.0f}".format)  # Currency, no decimals
        income_metrics_df["Ending Value"] = income_metrics_df["Ending Value"].map("${:,.0f}".format)  # Currency, no decimals
        income_metrics_df["Current Income"] = income_metrics_df["Current Income"].map("${:,.0f}".format)  # Currency, no decimals
        income_metrics_df["Current Income as % of Original Investment"] = income_metrics_df[
            "Current Income as % of Original Investment"
        ].map("{:.2f}%".format)  # Percentage, two decimals

        # Format the table using the utility function (optional if required for uniform styling)
        formatted_income_metrics_df = format_table(income_metrics_df)

        return formatted_income_metrics_df

    except Exception as e:
        raise RuntimeError(f"Error calculating income metrics: {e}")