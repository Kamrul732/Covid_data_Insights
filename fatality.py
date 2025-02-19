import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns

conn = psycopg2.connect(
    dbname="covid_db1",  # Change this to your database name
    user="postgres",  # Change this to your username
    password="41kamal",  # Change this to your password
    host="localhost",  # Change this if your database is remote
    port="5432"
)

query = """
SELECT "Date", "Country/Region", "Confirmed", "Deaths", "Recovered"
FROM covid_cases
ORDER BY "Date";
"""

df = pd.read_sql(query, conn)
conn.close()

df["Date"] = pd.to_datetime(df["Date"])

regional_trends = df.groupby(["Country/Region", "Date"])[["Confirmed", "Deaths", "Recovered"]].sum().reset_index()

top_regions = ["US", "India", "Brazil", "Russia", "UK"]  # Modify based on your dataset
plt.figure(figsize=(14, 7))

for region in top_regions:
    region_data = regional_trends[regional_trends["Country/Region"] == region]
    plt.plot(region_data["Date"], region_data["Deaths"], label=f"{region} - Deaths")

plt.title("COVID-19 Fatality Trends by Region")
plt.xlabel("Date")
plt.ylabel("Death Count")
plt.legend()
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(14, 7))

for region in top_regions:
    region_data = regional_trends[regional_trends["Country/Region"] == region]
    plt.plot(region_data["Date"], region_data["Recovered"], label=f"{region} - Recovered")

plt.title("COVID-19 Recovery Trends by Region")
plt.xlabel("Date")
plt.ylabel("Recovered Cases")
plt.legend()
plt.xticks(rotation=45)
plt.show()
