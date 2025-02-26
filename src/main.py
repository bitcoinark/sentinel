import json
import os
import logging
from dotenv import load_dotenv
from blockchain import BlockchainChecker
from notifier import Notifier
from scheduler import Scheduler

# Load environment variables
load_dotenv()

# Load config from file
with open("config/config.json", "r") as f:
    config = json.load(f)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("sentinel.log"),   # Log to file
        logging.StreamHandler()                # Log to Console
    ]
)
logger = logging.getLogger("Sentinel")

def main():
    # Initialize components with logger
    blockchain = BlockchainChecker(
        rpc_url=config["rpc_url"],
        electrs_url=config["electrs_url"],
        txid=config["txid"],
        vout=config["vout"],
        logger=logger
    )
    notifier = Notifier(
        email_to=config["email_to"],
        sms_to=config["sms_to"],
        smtp_user=os.getenv("SMTP_USER"),
        smtp_pass=os.getenv("SMTP_PASS"),
        twilio_sid=os.getenv("TWILIO_SID"),
        twilio_token=os.getenv("TWILIO_TOKEN"),
        twilio_from=os.getenv("TWILIO_FROM"),
        logger=logger
    )
    scheduler = Scheduler(
        blockchain=blockchain,
        notifier=notifier,
        cadence_seconds=config["cadence_seconds"],
        logger=logger
    )

    # Start the scheduler
    logger.info("Sentinel started. Monitoring UTXO...")
    scheduler.run()

if __name__ == "__main__":
    main()
