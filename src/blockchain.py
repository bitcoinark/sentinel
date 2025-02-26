from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

class BlockchainChecker:
    def __init__(self, rpc_url, txid, vout):
        self.rpc = AuthServiceProxy(rpc_url)
        self.txid = txid
        self.vout = vout
        self.last_status = "unspent"  # Initial assumption

    def is_utxo_unspent(self):
        """Check if the UTXO is still unspent."""
        try:
            result = self.rpc.gettxout(self.txid, self.vout)
            return result is not None  # Returns None if spent, dict if unspent
        except JSONRPCException as e:
            print(f"RPC error: {e}")
            return None  # Handle error gracefully

    def check_utxo(self):
        """Check UTXO status and return True if it was just spent."""
        current_status = self.is_utxo_unspent()
        if current_status is None:  # Error case
            return False
        if self.last_status == "unspent" and not current_status:
            self.last_status = "spent"
            return True  # Just spent
        self.last_status = "unspent" if current_status else "spent"
        return False
