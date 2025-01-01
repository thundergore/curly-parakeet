# visualisation.py
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import argparse
import shutil

def load_data(test_mode=False):
    # Determine the file path based on the mode
    if test_mode:
        csv_path = 'dummy_data/dummy_data.csv'
    else:
        csv_path = os.getenv('CSV_OUTPUT_PATH', 'data/latest_data.csv')

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at {csv_path}")
    
    return pd.read_csv(csv_path)

def setup_test_environment():
    # Test-specific output folder
    test_output_folder = 'test_visualisations'
    if os.path.exists(test_output_folder):
        shutil.rmtree(test_output_folder)  # Remove existing test folder and contents
    os.makedirs(test_output_folder)  # Create a fresh test folder
    return test_output_folder

def filter_factions(df, factions):
    if factions:
        filtered_df = df[df['faction'].isin(factions)]
        if filtered_df.empty:
            available_factions = df['faction'].unique().tolist()
            raise ValueError(f"No matching factions found for: {', '.join(factions)}. Available factions are: {', '.join(available_factions)}")
        return filtered_df
    return df

def create_visualisations(df, test_mode=False):
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
