# Cart2Insights
### Decoding E-Commerce Performance

## Project Overview
Cart2Insights is an end-to-end e-commerce analytics project
that transforms transactional data into business insights
using Python, SQL, feature engineering, statistical analysis
and an interactive Streamlit dashboard.

## Technologies Used
- Python
- Pandas and NumPy
- SQL and SQLite
- Streamlit
- Statistical Analysis
- Google Colab

## Dashboard Sections
1. Business Overview
2. Sales Analysis
3. Customer Analysis
4. Seller & Product Analysis
5. Delivery Analysis
6. Customer Experience

## Feature Engineering
- Total order value
- Total freight value
- Total items per order
- Delivery duration and delay
- Customer order count and spending
- Customer average order value
- Repeat customer indicator
- Seller revenue and order count

## Statistical Analysis
- Welch's t-test: Delayed vs on-time order review scores
- One-way ANOVA: Average order value across product categories

These comparisons are observational and do not establish causation.

## Run the Dashboard

Install dependencies:

pip install -r requirements.txt

Start the application:

streamlit run app.py

## Data Notes
The dashboard uses cleaned datasets stored in the project repository.

Sales figures are based on item prices and are not profit.

Delivery analysis uses records with valid required timestamps.

## Project Purpose
To demonstrate an end-to-end data analytics workflow
and communicate e-commerce business performance through
an interactive dashboard.
