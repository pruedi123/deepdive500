import pandas as pd
from ltc_bonds import calculate_non_reinvesting_strategy, calculate_reinvesting_strategy
from divs import calculate_dividends


def create_comparison_table(
    sp500_data, bond_data, initial_investment, begin_date, end_date, data_type="Nominal", cpi_data=None
):
    """
    Creates a comparison table for SP500 and Bond investments.

    Parameters:
        sp500_data (pd.DataFrame): DataFrame containing SP500 data.
        bond_data (pd.DataFrame): DataFrame containing bond data.
        initial_investment (float): Initial investment amount.
        begin_date (str): Begin date for filtering data in 'YYYY-MM' format.
        end_date (str): End date for filtering data in 'YYYY-MM' format.
        data_type (str): Type of data ("Nominal" or "Real").
        cpi_data (pd.DataFrame): DataFrame containing CPI data with 'Date' and 'CPI' columns.

    Returns:
        pd.DataFrame: A DataFrame representing the comparison table.
    """
    try:
        # Retrieve data for SP500
        dividend_results = calculate_dividends(
            sp500_data, start_date=begin_date, end_date=end_date, initial_investment=initial_investment
        )

        if data_type == "Nominal":
            sp500_non_reinvested = dividend_results["Nominal_No_Reinvestment"][2]
            sp500_with_reinvestment = dividend_results["Nominal_With_Reinvestment"][2]
        elif data_type == "Real":
            sp500_non_reinvested = dividend_results["Real_No_Reinvestment"][2]
            sp500_with_reinvestment = dividend_results["Real_With_Reinvestment"][2]
        else:
            raise ValueError(f"Invalid data_type: {data_type}")

        if bond_data.empty:
            # Partial table if no bond data is available
            comparison_data = {
                "Strategy": [
                    f"{data_type} SP500 Investment–No Reinvestment",
                    f"{data_type} Bonds Investment–No Reinvestment",
                    f"{data_type} SP500 Investment–With Reinvestment",
                    f"{data_type} Bonds Investment–With Reinvestment",
                ],
                "Total Dividends/Interest": [
                    f"${dividend_results[f'{data_type}_No_Reinvestment'][1]:,.0f}",
                    "NA",
                    "NA",
                    "NA",
                ],
                "Ending Value": [
                    f"${sp500_non_reinvested:,.0f}",
                    "NA",
                    f"${sp500_with_reinvestment:,.0f}",
                    "NA",
                ],
            }
        else:
            # Calculate bond metrics
            non_reinvesting_metrics = calculate_non_reinvesting_strategy(bond_data, initial_investment)
            reinvesting_metrics = calculate_reinvesting_strategy(bond_data, initial_investment)

            if data_type == "Nominal":
                total_interest_bonds_non_reinvested = non_reinvesting_metrics["Total Interest Paid (Nominal)"] / 12
                bond_ending_value_non_reinvested = non_reinvesting_metrics["Ending Value (Nominal)"]
                bond_ending_value_reinvested = reinvesting_metrics["Ending Value (Nominal)"]
            elif data_type == "Real":
                total_interest_bonds_non_reinvested = non_reinvesting_metrics["Total Interest Paid (Real)"] / 12
                bond_ending_value_non_reinvested = non_reinvesting_metrics["Ending Value (Real)"]
                bond_ending_value_reinvested = reinvesting_metrics["Ending Value (Real)"]

                # Adjust Real Bonds Investment–No Reinvestment Ending Value by CPI
                if cpi_data is not None:
                    cpi_data['Date'] = pd.to_datetime(cpi_data['Date'], errors='coerce').dt.strftime('%Y-%m')
                    cpi_data = cpi_data.dropna(subset=['Date'])
                    
                    cpi_filtered = cpi_data[
                        (cpi_data['Date'] >= begin_date) & (cpi_data['Date'] <= end_date)
                    ]
                    if not cpi_filtered.empty:
                        cpi_begin = cpi_filtered.iloc[0]['CPI']
                        cpi_end = cpi_filtered.iloc[-1]['CPI']
                        cpi_increase_factor = cpi_end / cpi_begin if cpi_begin > 0 else 1
                        bond_ending_value_non_reinvested /= cpi_increase_factor

            # Construct the comparison table
            comparison_data = {
                "Strategy": [
                    f"{data_type} SP500 Investment–No Reinvestment",
                    f"{data_type} Bonds Investment–No Reinvestment",
                    f"{data_type} SP500 Investment–With Reinvestment",
                    f"{data_type} Bonds Investment–With Reinvestment",
                ],
                "Total Dividends/Interest": [
                    f"${dividend_results[f'{data_type}_No_Reinvestment'][1]:,.0f}",
                    f"${total_interest_bonds_non_reinvested:,.0f}",
                    "NA",
                    "NA",
                ],
                "Ending Value": [
                    f"${sp500_non_reinvested:,.0f}",
                    f"${bond_ending_value_non_reinvested:,.0f}",
                    f"${sp500_with_reinvestment:,.0f}",
                    f"${bond_ending_value_reinvested:,.0f}",
                ],
            }

        # Convert to DataFrame
        comparison_table = pd.DataFrame(comparison_data)
        return comparison_table

    except Exception as e:
        raise RuntimeError(f"Error creating the comparison table: {e}")