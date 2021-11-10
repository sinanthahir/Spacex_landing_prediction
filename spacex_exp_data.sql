-- shows all the table
SELECT * 
FROM SPACEXTBL


-- Display the names of the unique launch sites in the space mission
SELECT DISTINCT LAUNCH_SITE
FROM SPACEXTBL


-- Display 5 records where launch sites begin with the string 'CCA'
SELECT *
FROM SPACEXTBL
WHERE LAUNCH_SITE LIKE 'CCA%'
LIMIT 5


-- Display the total payload mass carried by booster version 'F9 v1.1'
SELECT SUM(PAYLOAD_MASS_KG_) AS Total_Payload_NASA_CRS
FROM SPACEXTBL
WHERE BOOSTER_VERSION = 'F9 v1.1' 


-- Display average payload mass carried by booster version F9 v1.1
SELECT AVG(PAYLOAD_MASS_KG_) AS Average_Payload_F9_v11
FROM SPACEXTBL
WHERE BOOSTER_VERSION = 'F9 v1.1'


-- List the date when the first successful landing outcome in ground pad was achieved
SELECT DATE 
FROM SPACEXTBL
WHERE LANDING_OUTCOME LIKE '%ground pad%'
    AND MISSION_OUTCOME = 'Success'
ORDER BY DATE ASC
LIMIT 1


-- ALternate using MIN function
SELECT MIN(DATE)
FROM SPACEXTBL
WHERE LANDING_OUTCOME LIKE '%ground pad%'
    AND MISSION_OUTCOME= 'Success'


-- List the names of the boosters which have success in drone ship and have payload mass greater than 4000 but less than 6000
SELECT BOOSTER_VERSION
FROM SPACEXTBL
WHERE LANDING_OUTCOME LIKE '%drone ship%'
    AND MISSION_OUTCOME = 'Success'
    AND PAYLOAD_MASS_KG_ BETWEEN 4000 AND 6000


-- List the total number of successful and failure mission outcomes
SELECT MISSION_OUTCOME, COUNT(MISSION_OUTCOME) AS TOTAL 
FROM SPACEXTBL
GROUP BY MISSION_OUTCOME


-- List the names of the booster_versions which have carried the maximum payload mass. Use a subquery
SELECT BOOSTER_VERSION
FROM SPACEXTBL
WHERE (SELECT MAX(PAYLOAD_MASS_KG_) FROM SPACEXTBL) = PAYLOAD_MASS_KG_


-- List the failed landing_outcomes in drone ship, their booster versions, and launch site names for in year 2015
SELECT BOOSTER_VERSION, LAUNCH_SITE
FROM SPACEXTBL
WHERE LANDING_OUTCOME = 'Failure (drone ship)'
    AND DATE LIKE '%2015%'


-- Rank the count of landing outcomes (such as Failure (drone ship) or Success (ground pad)) between the date 2010-06-04 and 2017-03-20, in descending order
SELECT LANDING_OUTCOME, COUNT(LANDING_OUTCOME) AS TOTAL
FROM SPACEXTBL
WHERE DATE BETWEEN '2010-06-04' AND '2017-03-20'
GROUP BY LANDING_OUTCOME
ORDER BY TOTAL DESC

