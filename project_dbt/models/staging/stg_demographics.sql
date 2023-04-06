{{ config(materialized='table') }}

SELECT 
    _id as id,
    age_group,
    client_gender
FROM `covid-19-toronto.covid19_toronto.covid_data`