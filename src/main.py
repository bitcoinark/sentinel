import json
import os
from dotenv import load_dotenv
from blockchain import BlockchainChecker
from notifier import Notifier
from scheduler import Scheduler

# Load environment variables
load_dotenv()

# Load config from file
with open("config/config.json", "r") as f:
    config = json.load(f)

def main():
    # Initialize components
    blockchain = BlockchainChecker(
        rpc_url=config["rpc_url"],
        txid=config["txid"],
        vout=config["vout"]
    )
    notifier = Notifier(
        email_to=config["email_to"],
        sms_to=config["sms_to"],
        smtp_user=os.getenv("SMTP_USER"),
        smtp_pass=os.getenv("SMTP_PASS"),
        twilio_sid=os.getenv("TWILIO_SID"),
        twilio_token=os.getenv("TWILIO_TOKEN"),
        twilio_from=os.getenv("TWILIO_FROM")
    )
    scheduler = Scheduler(
        blockchain=blockchain,
        notifier=notifier,
        cadence_seconds=config["cadence_seconds"]
    )

    # Start the scheduler
    print("Sentinel started. Monitoring UTXO...")
    scheduler.run()

if __name__ == "__main__":
    main()
