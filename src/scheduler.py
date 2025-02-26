import time

class Scheduler:
    def __init__(self, blockchain, notifier, cadence_seconds):
        self.blockchain = blockchain
        self.notifier = notifier
        self.cadence_seconds = cadence_seconds

    def run(self):
        """Run the monitoring loop indefinitely."""
        while True:
            if self.blockchain.check_utxo():
                self.notifier.notify(self.blockchain.txid, self.blockchain.vout)
            time.sleep(self.cadence_seconds)
