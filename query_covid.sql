SELECT * FROM covid_cases LIMIT 10;
SELECT * FROM covid_cases LIMIT 10;

SELECT 
    "Country/Region", 
    MAX("Confirmed") AS total_cases, 
    MAX("Deaths") AS total_deaths, 
    MAX("Recovered") AS total_recovered
FROM covid_cases
GROUP BY "Country/Region"
ORDER BY total_cases DESC;

SELECT 
    "Country/Region",
    "Date",
    "Confirmed",
    LAG("Confirmed") OVER (PARTITION BY "Country/Region" ORDER BY "Date") AS previous_day_cases,
    ("Confirmed" - LAG("Confirmed") OVER (PARTITION BY "Country/Region" ORDER BY "Date")) AS new_cases
FROM covid_cases
ORDER BY "Country/Region", "Date";
