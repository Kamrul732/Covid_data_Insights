import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns

# **Step 1: Connect to PostgreSQL Database**
conn = psycopg2.connect(
    dbname="covid_db1",  # Change this to your database name
    user="postgres",  # Change this to your username
    password="41kamal",  # Change this to your password
    host="localhost",  # Change this if your database is remote
    port="5432"
)

# **Step 2: Fetch COVID-19 Data from PostgreSQL**
query = """
SELECT "Date", "Country/Region", "Confirmed", "Deaths", "Recovered"
FROM covid_cases
ORDER BY "Date";
"""

df = pd.read_sql(query, conn)
conn.close()

df["Date"] = pd.to_datetime(df["Date"])

# **Step 4: Group Data by Region to Analyze Trends**
regional_trends = df.groupby(["Country/Region", "Date"])[["Confirmed", "Deaths", "Recovered"]].sum().reset_index()

# **Step 5: Visualize Infection Trends for a Few Major Regions**
top_regions = ["US", "India", "Brazil", "Russia", "UK"]  # Modify based on your dataset

plt.figure(figsize=(14, 7))
for region in top_regions:
    region_data = regional_trends[regional_trends["Country/Region"] == region]
    plt.plot(region_data["Date"], region_data["Confirmed"], label=region)

plt.title("COVID-19 Infection Trends by Region")
plt.xlabel("Date")
plt.ylabel("Confirmed Cases")
plt.legend()
plt.xticks(rotation=45)
plt.show()