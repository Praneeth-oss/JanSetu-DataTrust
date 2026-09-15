-- JANSETU DATA TRUST
-- SQL Analytics

-- 1. Records by state
SELECT
    state,
    COUNT(*) AS record_count
FROM public_service_records
GROUP BY state
ORDER BY record_count DESC;


-- 2. Records by department
SELECT
    department,
    COUNT(*) AS record_count
FROM public_service_records
GROUP BY department
ORDER BY record_count DESC;


-- 3. Average annual income by state
SELECT
    state,
    ROUND(AVG(annual_income), 2) AS average_income
FROM public_service_records
GROUP BY state
ORDER BY average_income DESC;


-- 4. Service-request volume by department
SELECT
    department,
    SUM(service_requests) AS total_service_requests,
    ROUND(AVG(service_requests), 2) AS average_requests
FROM public_service_records
GROUP BY department
ORDER BY total_service_requests DESC;


-- 5. Records with unusually high service-request volume
SELECT
    record_id,
    state,
    department,
    service_requests
FROM public_service_records
WHERE service_requests >= 20
ORDER BY service_requests DESC;


-- 6. Missing-value summary
SELECT
    SUM(CASE WHEN age IS NULL THEN 1 ELSE 0 END) AS missing_age,
    SUM(CASE WHEN state IS NULL THEN 1 ELSE 0 END) AS missing_state,
    SUM(CASE WHEN annual_income IS NULL THEN 1 ELSE 0 END) AS missing_income,
    SUM(CASE WHEN email IS NULL THEN 1 ELSE 0 END) AS missing_email,
    SUM(CASE WHEN phone IS NULL THEN 1 ELSE 0 END) AS missing_phone
FROM public_service_records;