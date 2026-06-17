-- Create services registry
CREATE TABLE services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
) ENGINE=InnoDB;

-- Create logs table
-- Added indexes for faster filtering (by service and log level)
CREATE TABLE logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    service_id INT NOT NULL,
    level VARCHAR(10) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed TINYINT(1) DEFAULT 0, -- 0 = not processed, 1 = processed
    FOREIGN KEY (service_id) REFERENCES services(id),
    
    -- Indexes to speed up work
    INDEX idx_service_level (service_id, level),
    INDEX idx_created_at (created_at),
    INDEX idx_processed (processed)
) ENGINE=InnoDB;

-- Create alerts table
-- Added ON DELETE CASCADE: if a log is deleted, the corresponding alert is also removed
CREATE TABLE alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    log_id INT NOT NULL,
    status VARCHAR(50),
    recipient VARCHAR(255),
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (log_id) REFERENCES logs(id) ON DELETE CASCADE
) ENGINE=InnoDB;

