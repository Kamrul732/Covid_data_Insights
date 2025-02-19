import pandas as pd
from sqlalchemy import create_engine

# Load datasets
confirmed_df = pd.read_csv("/Users/mdkamrulhasan/Desktop/DataScience/project2/COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
deaths_df = pd.read_csv("/Users/mdkamrulhasan/Desktop/DataScience/project2/COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
recovered_df = pd.read_csv("/Users/mdkamrulhasan/Desktop/DataScience/project2/COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")


def clean_transform(df, value_name):
    df = df.melt(id_vars=["Province/State", "Country/Region", "Lat", "Long"],
                 var_name="Date",
                 value_name=value_name)
    df["Date"] = pd.to_datetime(df["Date"])  # Convert to datetime
    return df

confirmed_df = clean_transform(confirmed_df, "Confirmed")
deaths_df = clean_transform(deaths_df, "Deaths")
recovered_df = clean_transform(recovered_df, "Recovered")

covid_data = confirmed_df.merge(deaths_df, on=["Province/State", "Country/Region", "Lat", "Long", "Date"])
covid_data = covid_data.merge(recovered_df, on=["Province/State", "Country/Region", "Lat", "Long", "Date"])

covid_data.fillna({"Province/State": "Unknown"}, inplace=True)

print(covid_data.head())

covid_data.to_csv("cleaned_covid_data.csv", index=False)
DB_CONNECTION = "postgresql://mdkamrulhasan:41kamal@localhost:5432/covid_db1"
engine = create_engine(DB_CONNECTION)

covid_data.to_sql("covid_cases", engine, if_exists="replace", index=False)

print("Data successfully saved to PostgreSQL.")
