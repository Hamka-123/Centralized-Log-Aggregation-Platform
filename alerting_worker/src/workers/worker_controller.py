import time
import logging
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)
class WorkerController:
    def __init__(self, engine, config):
        self.engine = engine
        self.interval = config.POLLING_INTERVAL
        self.max_workers = config.WORKER_MAX_THREADS

    def start(self):
        logger.info(f"Alert Worker started with {self.max_workers} threads...")
    
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while True:
                executor.submit(self.engine.process_alerts)

                time.sleep(self.interval)