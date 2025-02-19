import pandas as pd
import psycopg2
import plotly.express as px
from prophet import Prophet
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

def fetch_data():
    conn = psycopg2.connect(
        dbname="covid_db1",  # Change this to your actual database
        user="postgres",  # Change this
        password="41kamal",  # Change this
        host="localhost",  # Keep as localhost if local
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
    return df

df = fetch_data()
df["Date"] = pd.to_datetime(df["Date"])

countries = df["Country/Region"].unique()


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("COVID-19 Recovery Prediction Dashboard", style={'textAlign': 'center'}),
    
    html.Label("Select a Country:"),
    dcc.Dropdown(
        id="country-dropdown",
        options=[{"label": country, "value": country} for country in countries],
        value="US",  # Default country
        multi=False
    ),
    
    dcc.Graph(id="recovery-trend-graph"),
])

@app.callback(
    Output("recovery-trend-graph", "figure"),
    [Input("country-dropdown", "value")]
)
def update_graph(selected_country):
    
    country_data = df[df["Country/Region"] == selected_country]
    country_recovery = country_data.groupby("Date")["Recovered"].sum().reset_index()
    country_recovery.columns = ["ds", "y"]  # Prophet requires 'ds' (date) and 'y' (value)


    model = Prophet()
    model.fit(country_recovery)
    future = model.make_future_dataframe(periods=60)
    forecast = model.predict(future)

    # Plot Predictions
    fig = px.line(forecast, x="ds", y="yhat", labels={"ds": "Date", "yhat": "Predicted Recoveries"},
                  title=f"Predicted Recoveries for {selected_country}")

    return fig

# **Run the Dash App**
if __name__ == "__main__":
    app.run_server(debug=True)
