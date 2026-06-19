import smtplib
from email.message import EmailMessage
import logging

logger = logging.getLogger(__name__)

class SMTPClient:
    def __init__(self, config):
        self.config = config

    def send(self, subject, body):
        if str(self.config.get("DISABLE_SMTP", "false")).lower() in ["true", "1"]:
            logger.info(f"[MOCK] SMTP disabled. Skipping email: {subject}")
            return True
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = self.config['USER']
        msg['To'] = self.config['RECIPIENT']

        server_address = self.config['SERVER']
        server_port = int(self.config['PORT'])
        
        logger.info(f"Connecting to {server_address}:{server_port}...")

        server = smtplib.SMTP(server_address, server_port)
        
        server.set_debuglevel(1) 
        
        try:
            if server_address != "mailhog":
                server.starttls()
                server.login(self.config['USER'], self.config['PASSWORD'])
            server.send_message(msg)
            logger.info("Email sent successfully!")
        except Exception as e:
            logger.error(f"SMTP Error details: {e}")
            raise e
        finally:
            server.quit()