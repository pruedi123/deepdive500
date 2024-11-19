import pandas as pd

def format_table(dataframe, start_at_one=True):
    """
    Format the DataFrame for display in Streamlit.

    Parameters:
    - dataframe (pd.DataFrame): The DataFrame to format.
    - start_at_one (bool): Whether to reset the index starting at 1. If False, no index is displayed.

    Returns:
    - pd.DataFrame.style: A styled DataFrame with alternating row colors and formatted index.
    """
    if start_at_one:
        # Reset index to start from 1
        dataframe = dataframe.reset_index(drop=True)
        dataframe.index += 1

    # Define alternating row colors
    styles = [
        dict(selector="tbody tr:nth-child(odd)", props=[("background-color", "#f9f9f9")]),
        dict(selector="tbody tr:nth-child(even)", props=[("background-color", "#e0f7fa")]),
    ]

    # Format missing values and apply styles
    styled = dataframe.style.set_table_styles(styles).format(na_rep="N/A")

    # Hide the index if not starting at one
    if not start_at_one:
        styled = styled.hide(axis="index")

    return styled