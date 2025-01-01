# visualisation.py
import pandas as pd
import plotly.express as px
import os

def load_data():
    # Load the data from the CSV file
    csv_path = os.getenv('CSV_OUTPUT_PATH', 'data/latest_data.csv')
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at {csv_path}")
    
    return pd.read_csv(csv_path)

def create_visualisation(df):
    # Example: Create a simple bar chart
    fig = px.bar(df, x=df.columns[0], y=df.columns[1], title="Data Visualisation")
    output_path = os.getenv('VISUAL_OUTPUT_PATH', 'visualisations/latest_visualisation.html')
    fig.write_html(output_path)
    print(f"Visualisation saved to {output_path}")

if __name__ == "__main__":
    data = load_data()
    create_visualisation(data)