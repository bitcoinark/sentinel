import pytest
from unittest.mock import Mock, patch
from blockchain import BlockchainChecker

@pytest.fixture
def logger():
    return Mock()

@pytest.fixture
def blockchain(logger):
    return BlockchainChecker(
        rpc_url="http://test:test@localhost:8332",
        electrs_url="http://localhost:50001",
        txid="abc123",
        vout=0,
        logger=logger
    )

def test_is_utxo_unspent_rpc_unspent(blockchain):
    with patch.object(blockchain.rpc, "gettxout", return_value={"value": 1.0}):
        assert blockchain.is_utxo_unspent_rpc() is True
        blockchain.logger.debug.assert_called_with("Checking UTXO with Bitcoin Core RPC")

def test_is_utxo_unspent_rpc_spent(blockchain):
    with patch.object(blockchain.rpc, "gettxout", return_value=None):
        assert blockchain.is_utxo_unspent_rpc() is False

def test_is_utxo_unspent_electrs_unspent(blockchain):
    mock_response_tx = {"vout": [{"scriptpubkey": "deadbeef"}]}
    mock_response_history = [{"tx_hash": "abc123"}]  # Only the original tx
    with patch("requests.get") as mock_get:
        mock_get.side_effect = [
            Mock(status_code=200, json=lambda: mock_response_tx),
            Mock(status_code=200, json=lambda: mock_response_history)
        ]
        assert blockchain.is_utxo_unspent_electrs() is True
        blockchain.logger.debug.assert_called_with("Checking UTXO with electrs")

def test_check_utxo_transition(blockchain):
    with patch.object(blockchain, "is_utxo_unspent", side_effect=[True, False]):
        assert blockchain.check_utxo() is False  # Still unspent
        assert blockchain.check_utxo() is True   # Just spent
        blockchain.logger.info.assert_called_with("UTXO spent: txid=abc123, vout=0")
