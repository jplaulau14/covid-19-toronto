{{ config(materialized='table') }}

SELECT 
    _id as id,
    neighbourhood_name,
    fsa
FROM `covid-19-toronto.covid19_toronto.covid_data`
WHERE fsa IS NOT NULL
