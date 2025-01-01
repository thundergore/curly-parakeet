
# PostgreSQL Dashboard Visualization Script

This script generates visualizations from PostgreSQL data for factions in a tabletop gaming context. The visualizations include dual-axis charts for performance metrics and rank tables based on faction statistics.

## Features
- Supports both **charts** and **rank table** visualizations.
- Allows filtering by one or more factions.
- Offers a **test mode** to run the script with dummy data.
- Saves visualizations as HTML files for easy sharing and review.

## Arguments
### `--test`
- **Description**: Run the script in test mode using dummy data.
- **Purpose**: Useful for quickly testing output without requiring real data or environment variables.
- **Example**:
  ```bash
  python visualisation.py --test
  ```

### `--faction`
- **Description**: Filter by one or more faction names.
- **Purpose**: Focuses the visualization on specific factions. If no factions are specified, all factions will be included.
- **Example**:
  ```bash
  python visualisation.py --faction "Maggotkin Of Nurgle" "Stormcast Eternals"
  ```
- **Error Handling**: If no matching factions are found, the script will list available factions.

### `--viz`
- **Description**: Specify the type of visualization to generate.
- **Options**:
  - `charts`: Generates dual-axis charts showing performance metrics (e.g., total games, win rate).
  - `rank`: Generates a rank table for the latest month, including rank changes.
- **Default**: `charts`
- **Example**:
  ```bash
  python visualisation.py --viz rank
  ```

## Usage Examples
1. **Run in Test Mode**:
   ```bash
   python visualisation.py --test
   ```

2. **Generate Charts for All Factions**:
   ```bash
   python visualisation.py --viz charts
   ```

3. **Generate Rank Table for Specific Factions**:
   ```bash
   python visualisation.py --viz rank --faction "Maggotkin Of Nurgle"
   ```

4. **Handle Non-Matching Factions**:
   If no matching factions are found, the script will raise an error and display available factions.

## Output
- **Charts**: Saved as `visualisations/overlayed_performance_metrics_dual_axes.html`.
- **Rank Table**: Saved as `visualisations/rank_table.html`.
- **Test Mode Outputs**: Saved in the `test_visualisations/` directory.

## Notes
- Ensure the required Python dependencies are installed:
  ```bash
  pip install pandas plotly
  ```
- The `dummy_data/` folder is used in test mode and must contain valid test data.
- The script handles both real and test data seamlessly, ensuring flexible usage for development and production environments.
