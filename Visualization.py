import pandas as pd
import snowflake.connector

# Establish a Snowflake connection
conn = snowflake.connector.connect(
    user='your_user',
    password='your_password',
    account='your_account',
    warehouse='your_warehouse',
    database='your_database',
    schema='your_schema'
)

# Query data
query = """
SELECT
    DATE,
    COUNTRY_REGION,
    SUM(CASES) AS total_cases,
    SUM(CASES_TOTAL) AS cumulative_cases,
    SUM(DEATHS) AS total_deaths,
    SUM(DEATHS_TOTAL) AS cumulative_deaths
FROM
    WHO_DAILY_REPORT
GROUP BY
    DATE, COUNTRY_REGION
ORDER BY
    DATE, COUNTRY_REGION;
"""
df = pd.read_sql(query, conn)

# Close connection
conn.close()

import plotly.express as px

# Create visualizations
fig_cases = px.line(df, x='DATE', y='total_cases', color='COUNTRY_REGION', title='Daily New Cases')
fig_deaths = px.line(df, x='DATE', y='total_deaths', color='COUNTRY_REGION', title='Daily New Deaths')

# Save visualizations to HTML files
fig_cases.write_html('daily_new_cases.html')
fig_deaths.write_html('daily_new_deaths.html')

