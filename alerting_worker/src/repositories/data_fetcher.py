import pymysql
import logging

logger = logging.getLogger(__name__)

class DataFetcher:
    def __init__(self, db_factory):
        self.db_factory = db_factory

    def get_unprocessed_logs(self):
        """Returns a list of logs to be processed."""
        conn = self.db_factory() # Create a connection inside the method for thread safety
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                # We take only those that processed = 0
                query = "SELECT * FROM logs WHERE processed = 0 AND level IN ('ERROR', 'CRITICAL')"
                cursor.execute(query)
                logs = cursor.fetchall()
                logger.info(f"Fetched {len(logs)} logs.")
                return logs
        finally:
            conn.close() 

    def try_claim_log(self, log_id):
        """Atomically marks the log as 'processing' (processed=1) to prevent other threads from picking it up."""
        conn = self.db_factory()
        try:
            with conn.cursor() as cursor:
                # IMPORTANT: Atomic update. If it returns 1, it means we've captured the log.
                # If 0, it means another thread managed to grab it first.
                sql = "UPDATE logs SET processed = 1 WHERE id = %s AND processed = 0"
                affected_rows = cursor.execute(sql, (log_id,))
                conn.commit()
                return affected_rows > 0
        finally:
            conn.close()

    def mark_as_alerted(self, log_id, status='SENT'):
        """Writes the processing result to the alerts table."""
        conn = self.db_factory()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO alerts (log_id, status) VALUES (%s, %s)", 
                    (log_id, status)
                )
            conn.commit()
        finally:
            conn.close()