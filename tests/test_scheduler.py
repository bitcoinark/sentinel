import pytest
from unittest.mock import Mock, patch
from scheduler import Scheduler

@pytest.fixture
def logger():
    return Mock()

@pytest.fixture
def scheduler():
    blockchain = Mock()
    notifier = Mock()
    return Scheduler(blockchain, notifier, cadence_seconds=1, logger=logger)

def test_run_checks_utxo(scheduler):
    scheduler.blockchain.check_utxo.return_value = True
    with patch("time.sleep") as mock_sleep:
        scheduler.run()  # Will loop forever, so patch sleep to break after one
        mock_sleep.side_effect = [None, KeyboardInterrupt]
        scheduler.logger.debug.assert_called_with("Checking UTXO status")
        scheduler.notifier.notify.assert_called()
