# PostgreSQL Dashboard on GitHub Pages

This project automates daily queries to a PostgreSQL database and updates a dashboard hosted on GitHub Pages. The dashboard provides interactive visualizations based on the latest data and is designed as a proof-of-concept for showcasing data insights.

## Features
- Automatically queries a PostgreSQL database using GitHub Actions.
- Processes and saves extracted data as CSV files.
- Updates an interactive dashboard hosted on GitHub Pages.
- Fully automated workflow, running daily.

## How It Works
1. A GitHub Actions workflow queries the PostgreSQL database and retrieves the latest data.
2. The data is saved as a static CSV file locally.
3. The GitHub Pages dashboard dynamically reads and visualizes the data.

## Usage
- **Public Repository**: The dashboard is publicly accessible at [GitHub Pages URL](https://<your-username>.github.io/<repo-name>).

## Development
- Clone the repository to modify the dashboard or the query logic.
- Update the SQL query in `queries/query_file.sql` for custom database queries. This file is ignored by Git to prevent sensitive information from being shared.
- Configure the environment variables in your local environment:
  - `CSV_OUTPUT_PATH`: (Optional) Specifies the file path where the output CSV should be saved. Defaults to `data/latest_data.csv` if not set.
  - `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: Required for connecting to the PostgreSQL database.
- Customize the dashboard visuals in the `index.html` file.

## Security
- Data is sanitized and aggregated to ensure no sensitive information is exposed.

---
