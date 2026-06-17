-- 1. Create services registry
CREATE TABLE IF NOT EXISTS services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
) ENGINE=InnoDB;

-- 2. Create logs table
-- Indexes included to accelerate search for unprocessed errors (Worker)
CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    service_id INT NOT NULL,
    level VARCHAR(10) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed TINYINT(1) DEFAULT 0, -- 0 = not processed, 1 = processed
    
    FOREIGN KEY (service_id) REFERENCES services(id),
    
    -- Indexes for query optimization
    INDEX idx_service_level (service_id, level),
    INDEX idx_created_at (created_at), -- Required for retention policy
    INDEX idx_processed_level (processed, level) -- Optimization for worker selection
) ENGINE=InnoDB;

-- 3. Create alerts table
-- ON DELETE CASCADE ensures automatic deletion of alerts when a log is deleted
CREATE TABLE IF NOT EXISTS alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    log_id INT NOT NULL,
    status VARCHAR(50),
    recipient VARCHAR(255),
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (log_id) REFERENCES logs(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 4. Create maintenance procedure
-- Encapsulated logic for log cleanup for better testability
DELIMITER //
CREATE PROCEDURE sp_cleanup_logs()
BEGIN
    DELETE FROM logs 
    WHERE created_at < DATE_SUB(NOW(), INTERVAL 30 DAY);
END //
DELIMITER ;

-- 5. Configure Retention Policy
-- Enable event scheduler
SET GLOBAL event_scheduler = ON;

-- Create an event that calls the maintenance procedure once a day at 03:00
CREATE EVENT IF NOT EXISTS purge_old_logs
ON SCHEDULE EVERY 1 DAY
STARTS (CURRENT_DATE + INTERVAL 1 DAY + INTERVAL 3 HOUR)
DO CALL sp_cleanup_logs();