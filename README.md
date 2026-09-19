# Nassau Candy Route Analysis

## Project Overview

Nassau Candy Route Analysis is a data analytics project developed to analyze
sales, shipping, factory performance, regional performance, products, and
delivery routes of Nassau Candy distribution data.

The project uses Python for data cleaning and analysis and Streamlit for
building an interactive dashboard.

## Objectives

- Analyze Nassau Candy sales data.
- Clean and validate the dataset.
- Analyze shipping lead time.
- Identify route performance.
- Analyze factory-wise business performance.
- Analyze region-wise sales and profit.
- Analyze product performance.
- Analyze shipping modes.
- Build an interactive dashboard with filters.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Plotly
- Streamlit
- VS Code

## Dataset

The dataset contains 10,194 records and 18 original columns.

Important fields include:

- Order ID
- Order Date
- Ship Date
- Ship Mode
- Customer ID
- City
- State/Province
- Division
- Region
- Product ID
- Product Name
- Sales
- Units
- Gross Profit
- Cost

## Data Processing

The project performs the following data processing steps:

1. Loads the Nassau Candy dataset.
2. Checks missing values.
3. Checks duplicate records.
4. Converts order and shipping dates.
5. Validates date values.
6. Calculates shipping lead time.
7. Checks negative lead times.
8. Maps products to factories.
9. Creates route-level analysis.
10. Generates business performance summaries.

## Analysis Performed

### Route Analysis

- Top performing routes
- Bottom performing routes
- Average shipping lead time
- Route efficiency score

### Factory Analysis

- Total orders
- Total units
- Total sales
- Gross profit
- Total cost

### Region Analysis

- Orders by region
- Units by region
- Sales by region
- Gross profit by region

### Product Analysis

- Product-wise units
- Product-wise sales
- Product-wise gross profit

### Shipping Analysis

- Ship mode-wise orders
- Average shipping lead time
- Sales by shipping mode
- Gross profit by shipping mode

## Interactive Dashboard

The Streamlit dashboard provides interactive filters for:

- Factory
- Region
- Ship Mode

When a filter is changed, the dashboard dynamically updates:

- KPI values
- Charts
- Tables
- Business analysis results

## Project Structure

```text
Nassau_Candy_Route_Analysis/
│
├── data/
│   └── Nassau Candy Distributor.csv
│
├── outputs/
│   ├── cleaned_nassau_data.csv
│   ├── route_summary.csv
│   ├── region_summary.csv
│   └── ship_mode_summary.csv
│
├── analysis.py
├── eda.py
├── app.py
├── utils.py
├── requirements.txt
└── README.md