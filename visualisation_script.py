# visualisation.py
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import argparse
import shutil

def load_data(test_mode=False):
    """
    Load data from a CSV file.
    This function loads data from a CSV file. If `test_mode` is set to True, it loads data from a dummy CSV file 
    located at 'dummy_data/dummy_data.csv'. Otherwise, it loads data from 'latest_data.csv' located in the directory 
    specified by the environment variable 'CSV_OUTPUT_PATH'. If the environment variable is not set, it defaults to 
    the 'data' directory.
    Args:
        test_mode (bool): If True, load data from the dummy CSV file. Default is False.
    Returns:
        pandas.DataFrame: The data loaded from the CSV file.
    Raises:
        FileNotFoundError: If the specified CSV file does not exist.
    """
    # Determine the file path based on the mode
    if test_mode:
        csv_path = 'dummy_data/dummy_data.csv'
    else:
        csv_path = os.path.join(os.getenv('CSV_OUTPUT_PATH', 'data'), 'latest_data.csv')

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at {csv_path}")
    
    return pd.read_csv(csv_path)

def setup_test_environment():
    """
    Sets up the test environment by creating a fresh test-specific output folder.

    This function performs the following steps:
    1. Checks if a folder named 'test_visualisations' exists.
    2. If it exists, removes the folder and its contents.
    3. Creates a new 'test_visualisations' folder.

    Returns:
        str: The path to the test-specific output folder.
    """
    # Test-specific output folder
    test_output_folder = 'test_visualisations'
    if os.path.exists(test_output_folder):
        shutil.rmtree(test_output_folder)  # Remove existing test folder and contents
    os.makedirs(test_output_folder)  # Create a fresh test folder
    return test_output_folder

def filter_factions(df, factions):
    """
    Filters the DataFrame to include only the specified factions.

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
        factions (list): A list of faction names to filter by.

    Returns:
        pandas.DataFrame: The filtered DataFrame containing only the specified factions.

    Raises:
        ValueError: If no matching factions are found in the DataFrame.
    """
    if factions:
        filtered_df = df[df['faction'].isin(factions)]
        if filtered_df.empty:
            available_factions = df['faction'].unique().tolist()
            raise ValueError(f"No matching factions found for: {', '.join(factions)}. Available factions are: {', '.join(available_factions)}")
        return filtered_df
    return df

def create_visualisations(df, test_mode=False):
    """
    Generates visualizations for performance metrics including Win Rates and Total Games.

    Parameters:
    df (pandas.DataFrame): DataFrame containing the data to be visualized. 
                           Expected columns: 'month_formatted', 'win_rate', 'weighted_win_rate', 'total_games', 'faction'.
    test_mode (bool): If True, sets up a test environment for saving the visualizations. Default is False.

    Returns:
    None: The function saves the generated visualization as an HTML file in the specified output folder.

    The function creates an overlayed chart with dual Y-axes:
    - Left Y-axis: Total Games (Bar chart)
    - Right Y-axis: Win Rate and Weighted Win Rate (Line charts)

    The chart is saved as 'overlayed_performance_metrics_dual_axes.html' in the 'visualisations' folder or a test folder if test_mode is True.
    """
    output_folder = 'visualisations'

    if test_mode:
        output_folder = setup_test_environment()  # Set up test environment

    # Overlayed Chart with Dual Y-Axes for Win Rates and Total Games
    fig = go.Figure()

    # Add Win Rate to Right Y-Axis
    fig.add_trace(go.Scatter(
        x=df['month_formatted'], 
        y=df['win_rate'], 
        mode='lines+markers', 
        name='Win Rate',
        yaxis='y2',
        line=dict(color='red')
    ))

    # Add Weighted Win Rate to Right Y-Axis
    fig.add_trace(go.Scatter(
        x=df['month_formatted'], 
        y=df['weighted_win_rate'], 
        mode='lines+markers', 
        name='Weighted Win Rate',
        yaxis='y2',
        line=dict(color='green')
    ))

    # Add Total Games to Left Y-Axis
    fig.add_trace(go.Bar(
        x=df['month_formatted'], 
        y=df['total_games'], 
        name='Total Games',
        marker_color='blue',
        yaxis='y1'
    ))

    # Set Title, Axes, and Layout
    faction_name = df['faction'].iloc[0] if 'faction' in df.columns else "Unknown Faction"
    fig.update_layout(
        title=f"Performance Metrics for {faction_name}",
        xaxis_title="Month",
        yaxis=dict(
            title="Total Games",
            titlefont=dict(color="blue"),
            tickfont=dict(color="blue"),
            side="left",
        ),
        yaxis2=dict(
            title="Win Rates",
            titlefont=dict(color="black"),
            tickfont=dict(color="black"),
            overlaying="y",
            side="right",
        ),
        legend_title="Metrics",
        barmode='overlay'
    )

    fig_path = os.path.join(output_folder, 'overlayed_performance_metrics_dual_axes.html')
    fig.write_html(fig_path)
    print(f"Overlayed chart with dual axes saved to {fig_path}")

def create_rank_table(df, test_mode=False):
    output_folder = 'visualisations'

    if test_mode:
        output_folder = setup_test_environment()  # Set up test environment

    # Get the latest month
    latest_month = df['month_formatted'].max()

    # Filter data for the latest month
    latest_data = df[df['month_formatted'] == latest_month].copy()

    # Sort by rank
    latest_data.sort_values(by='monthly_rank', inplace=True)

    # Create table data
    table_data = {
        "Faction": latest_data['faction'],
        "Current Month": latest_data['month_formatted'],
        "Weighted Win Rate": latest_data['weighted_win_rate'].round(2),
        "Rank": latest_data['monthly_rank'],
        "Rank Change": latest_data['rank_change'].fillna(0).astype(int),
    }

    # Create Plotly Table
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["Faction", "Current Month", "Weighted Win Rate", "Rank", "Rank Change"],
            fill_color='paleturquoise',
            align='left'
        ),
        cells=dict(
            values=[table_data[key] for key in table_data.keys()],
            fill_color='lavender',
            align='left'
        )
    )])

    # Save the table as an HTML file
    fig_path = os.path.join(output_folder, 'rank_table.html')
    fig.write_html(fig_path)
    print(f"Rank table saved to {fig_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate visualisations from CSV data.")
    parser.add_argument("--test", action="store_true", help="Run the script in test mode using dummy data.")
    parser.add_argument("--faction", nargs='+', help="Filter by one or more faction names.")
    parser.add_argument("--viz", choices=['rank', 'charts'], default='charts', help="Type of visualisation to generate.")
    args = parser.parse_args()

    data = load_data(test_mode=args.test)

    # Filter by faction if specified
    data = filter_factions(data, args.faction)

    if args.viz == 'charts':
        create_visualisations(data, test_mode=args.test)
    elif args.viz == 'rank':
        create_rank_table(data, test_mode=args.test)
