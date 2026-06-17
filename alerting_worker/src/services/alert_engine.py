import logging

logger = logging.getLogger(__name__)

class AlertEngine:
    def __init__(self, fetcher, mailer):
        self.fetcher = fetcher
        self.mailer = mailer

    def process_alerts(self):
        try:
            # Fetch all potentially unprocessed logs
            logs = self.fetcher.get_unprocessed_logs()
        except Exception as e:
            logger.error(f"Failed to fetch logs: {e}")
            return 
        
        recipient = self.mailer.config.get('RECIPIENT', 'unknown')

        for log in logs:
            # 1. ATOMIC CLAIM: Try to reserve this log for this thread
            # If try_claim_log returns False, another thread already claimed it.
            if not self.fetcher.try_claim_log(log['id']):
                continue

            try:
                logger.info(f"Processing log {log['id']} in thread...")
                
                # 2. Send email
                subject = f"Alert: {log['level']} in service {log['service_name']} id: {log['service_id']} "
                body = (
                    f"ALERT DETAILS\n"
                    f"-----------------------------------------------\n"
                    f"Service/Component ID: {log.get('service_id', 'Unknown')}\n"
                    f"Severity Level:       {log.get('level', 'Unknown')}\n"
                    f"Timestamp:            {log.get('created_at', 'Not provided')}\n"
                    f"-----------------------------------------------\n\n"
                    f"Message Content:\n{log.get('message', 'No message content')}\n"
                )
                self.mailer.send(subject, body)
                
                # 3. Log success in the alerts table
                self.fetcher.mark_as_alerted(log['id'], recipient, status='SENT')
                logger.info(f"Successfully processed log {log['id']}")
                
            except Exception as e:
                # 4. Log failure (optional: mark as failed in the database)
                logger.exception(f"CRITICAL: Failed to process log {log['id']}.")
                self.fetcher.mark_as_alerted(log['id'], recipient, status='FAILED')