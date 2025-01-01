# query_db.py
import psycopg2
import pandas as pd
import os

# Database connection configuration
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

def query_postgresql():
    # Load the query from the SQL file
    query_file_path = os.path.join('queries', 'query_file.sql')
    with open(query_file_path, 'r') as file:
        query = file.read()

    # Connect to PostgreSQL
    with psycopg2.connect(**DB_CONFIG) as conn:
        # Load data into a Pandas DataFrame
        df = pd.read_sql(query, conn)

    return df


def save_to_csv(df):
    # Save the DataFrame to a CSV file
    output_path = os.getenv('CSV_OUTPUT_PATH', 'data/latest_data.csv')  # Uses the CSV_OUTPUT_PATH environment variable if set, otherwise defaults to 'data/latest_data.csv'
    df.to_csv(output_path, index=False)  # Overwrites the file
    print(f"Data saved to {output_path}")


if __name__ == "__main__":
    df = query_postgresql()
    save_to_csv(df)
