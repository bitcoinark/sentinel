import requests
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

class BlockchainChecker:
    def __init__(self, rpc_url, electrs_url, txid, vout, logger):
        self.rpc = AuthServiceProxy(rpc_url) if rpc_url else None
        self.electrs_url = electrs_url
        self.txid = txid
        self.vout = vout
        self.last_status = "unspent"
        self.logger = logger

    def is_utxo_unspent_rpc(self):
        """Check UTXO status using Bitcoin Core RPC."""
        try:
            result = self.rpc.gettxout(self.txid, self.vout)
            return result is not None  # Returns None if spent, dict if unspent
        except JSONRPCException as e:
            self.logger.error(f"RPC error: {e}")
            return None

    def is_utxo_unspent_electrs(self):
        """Check UTXO status using electrs REST API."""
        try:
            # Fetch transaction details
            tx_url = f"{self.electrs_url}/tx/{self.txid}"
            response = requests.get(tx_url)
            response.raise_for_status()
            tx = response.json()

            # Check if the output is spent (electrs doesn't directly provide gettxout-like status)
            # Use mempool or block height to infer if spent; this is a simplified check
            output = tx["vout"][self.vout]
            script_hash = output["scriptpubkey"][:64]  # Simplified, assumes hex
            history_url = f"{self.electrs_url}/scripthash/{script_hash}/history"
            history = requests.get(history_url).json()
            spent = any(h["tx_hash"] != self.txid for h in history)  # Spent if referenced elsewhere
            return not spent
        except requests.RequestException as e:
            self.logger.error(f"Electrs error: {e}")
            return None

    def is_utxo_unspent(self):
        """Check UTXO status, preferring electrs if available."""
        if self.electrs_url:
            self.logger.debug("Checking UTXO with electrs")
            return self.is_utxo_unspent_electrs()
        elif self.rpc:
            self.logger.debug("Checking UTXO with Bitcoin Core RPC")
            return self.is_utxo_unspent_rpc()
        self.logger.error("No blockchain source configured")
        return None
    
    def check_utxo(self):
        """Check UTXO status and return True if just spent."""
        current_status = self.is_utxo_unspent()
        if current_status is None:
            return False
        if self.last_status == "unspent" and not current_status:
            self.last_status = "spent"
            self.logger.info(f"UTXO spent: txid={self.txid"}, vout={self.vout}")
            return True
        self.last_status = "unspent" if current_status else "spent"
        return False
