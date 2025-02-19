import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

conn = psycopg2.connect(
    dbname="covid_db1",
    user="postgres",
    password="41kamal",
    host="localhost",
    port="5432"
)


query = """
SELECT "Date", "Country/Region", "Recovered"
FROM covid_cases
WHERE "Recovered" IS NOT NULL
ORDER BY "Date";
"""
df = pd.read_sql(query, conn)
conn.close()

df["Date"] = pd.to_datetime(df["Date"])

all_dates = pd.date_range(start=df["Date"].min(), end=df["Date"].max())
countries = df["Country/Region"].unique()

recovery_fixed = []

for country in countries:
    country_df = df[df["Country/Region"] == country].copy()
    
    # Create full date range
    country_dates = pd.DataFrame({"Date": all_dates})
    country_dates["Country/Region"] = country
    
    # Merge with recovery data
    merged = country_dates.merge(country_df, on=["Date", "Country/Region"], how="left")
    
    # **Ensure data is forward-filled correctly**
    merged["Recovered"] = merged["Recovered"].fillna(method="ffill")
    
    # **Ensure no remaining NaNs**
    merged["Recovered"] = merged["Recovered"].fillna(0)
    
    recovery_fixed.append(merged)


recovery_trends = pd.concat(recovery_fixed)
last_date = df["Date"].max()

top_regions = ["US", "India", "Brazil", "Russia", "UK"]

plt.figure(figsize=(14, 7))
for region in top_regions:
    region_data = recovery_trends[recovery_trends["Country/Region"] == region]
    plt.plot(region_data["Date"], region_data["Recovered"], label=region)

plt.axvline(x=last_date, color="red", linestyle="--", label="Last Data Available")

plt.title("COVID-19 Recovery Trends by Region")
plt.xlabel("Date")
plt.ylabel("Recovered Cases")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.show()
