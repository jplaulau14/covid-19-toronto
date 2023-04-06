{{ config(materialized='table') }}

SELECT
    _id as id,
    assigned_id,
    outbreak_associated,
    source_of_infection,
    classification,
    episode_date,
    reported_date,
    outcome,
    ever_hospitalized,
    ever_in_icu,
    ever_intubated
FROM `covid-19-toronto.covid19_toronto.covid_data`
