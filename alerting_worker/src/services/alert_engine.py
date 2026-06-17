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

        for log in logs:
            # 1. ATOMIC CLAIM: Try to reserve this log for this thread
            # If try_claim_log returns False, another thread already claimed it.
            if not self.fetcher.try_claim_log(log['id']):
                continue

            try:
                logger.info(f"Processing log {log['id']} in thread...")
                
                # 2. Send email
                subject = f"Alert: {log['level']} in service"
                body = f"Message: {log['message']}"
                self.mailer.send(subject, body)
                
                # 3. Log success in the alerts table
                self.fetcher.mark_as_alerted(log['id'], status='SENT')
                logger.info(f"Successfully processed log {log['id']}")
                
            except Exception as e:
                # 4. Log failure (optional: mark as failed in the database)
                logger.exception(f"CRITICAL: Failed to process log {log['id']}.")
                self.fetcher.mark_as_alerted(log['id'], status='FAILED')