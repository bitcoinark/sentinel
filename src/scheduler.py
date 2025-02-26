import time

class Scheduler:
    def __init__(self, blockchain, notifier, cadence_seconds, logger):
        self.blockchain = blockchain
        self.notifier = notifier
        self.cadence_seconds = cadence_seconds
        self.logger = logger

    def run(self):
        """Run the monitoring loop indefinitely."""
        while True:
            self.logger.debug("Checking UTXO status")
            if self.blockchain.check_utxo():
                self.notifier.notify(self.blockchain.txid, self.blockchain.vout)
            self.logger.debug(f"Sleeping for {self.cadence_seconds} seconds")
            time.sleep(self.cadence_seconds)
