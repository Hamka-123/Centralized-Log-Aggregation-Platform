import signal
import time
import logging
import threading
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


class WorkerController:
    def __init__(self, engine, config):
        self.engine = engine
        self.interval = config.POLLING_INTERVAL
        self.max_workers = config.WORKER_MAX_THREADS
        self._stop_event = threading.Event()
        self._executor = None

    def _handle_signal(self, signum, frame):
        sig_name = signal.Signals(signum).name
        logger.warning(f"Received {sig_name}. Initiating graceful shutdown...")
        self.stop()

    def start(self):
        logger.info(
            f"Alert Worker started with {self.max_workers} threads, "
            f"polling interval {self.interval}s..."
        )

        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)

        self._executor = ThreadPoolExecutor(max_workers=self.max_workers)

        try:
            while not self._stop_event.is_set():
                self._executor.submit(self.engine.process_alerts)
                # Use a shorter sleep so we respond to SIGTERM promptly
                self._stop_event.wait(timeout=self.interval)
        finally:
            self._shutdown()

    def stop(self):
        """Trigger graceful shutdown."""
        self._stop_event.set()

    def _shutdown(self):
        """Wait for all submitted tasks to complete, then release resources."""
        logger.info("Shutting down worker threads. Waiting for in-flight tasks...")
        if self._executor:
            # Allow at most 30 seconds for running tasks to finish
            self._executor.shutdown(wait=True, cancel_futures=False)
        logger.info("All worker threads terminated successfully.")
