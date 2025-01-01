# visualisation.py
import pandas as pd
import plotly.express as px
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

def create_visualisations(df, test_mode=False):
    output_folder = 'visualisations'

    if test_mode:
        output_folder = setup_test_environment()  # Set up test environment

    # 1. Line Chart for Total Games by Month
    fig1 = px.line(
        df, 
        x='month_formatted', 
        y='total_games', 
        title="Total Games by Month", 
        labels={"month_formatted": "Month", "total_games": "Total Games"}
    )
    fig1_path = os.path.join(output_folder, 'total_games_line.html')
    fig1.write_html(fig1_path)
    print(f"Line chart saved to {fig1_path}")

    # 2. Bar Chart for Win Rate by Month
    fig2 = px.bar(
        df, 
        x='month_formatted', 
        y='win_rate', 
        title="Win Rate by Month", 
        labels={"month_formatted": "Month", "win_rate": "Win Rate"}, 
        text='win_rate'
    )
    fig2.update_traces(texttemplate='%{text:.2%}', textposition='outside')
    fig2_path = os.path.join(output_folder, 'win_rate_bar.html')
    fig2.write_html(fig2_path)
    print(f"Bar chart saved to {fig2_path}")

    # 3. Scatter Plot for Weighted Win Rate vs. Rank Change
    fig3 = px.scatter(
        df, 
        x='weighted_win_rate', 
        y='rank_change', 
        color='month_formatted', 
        title="Weighted Win Rate vs. Rank Change", 
        labels={"weighted_win_rate": "Weighted Win Rate", "rank_change": "Rank Change"}
    )
    fig3_path = os.path.join(output_folder, 'weighted_win_vs_rank.html')
    fig3.write_html(fig3_path)
    print(f"Scatter plot saved to {fig3_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate visualisations from CSV data.")
    parser.add_argument("--test", action="store_true", help="Run the script in test mode using dummy data.")
    args = parser.parse_args()

    data = load_data(test_mode=args.test)
    create_visualisations(data, test_mode=args.test)
