-- 1. Total logs processed during the test
SELECT count(*) as total_logs FROM logs WHERE created_at > NOW() - INTERVAL 2 MINUTE;

-- 2. Performance per service
SELECT service_id, count(*) as log_count 
FROM logs 
WHERE created_at > NOW() - INTERVAL 2 MINUTE 
GROUP BY service_id;

-- 3. Status summary (Workload)
SELECT processed, count(*) as count 
FROM logs 
WHERE created_at > NOW() - INTERVAL 5 MINUTE 
GROUP BY processed;