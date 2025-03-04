import pytest
from unittest.mock import Mock, patch
from src.scheduler import Scheduler

@pytest.fixture
def logger():
    return Mock()

@pytest.fixture
def scheduler(logger):
    blockchain = Mock()
    notifier = Mock()
    return Scheduler(blockchain, notifier, cadence_seconds=1, logger=logger)

def test_run_checks_utxo(scheduler):
    scheduler.blockchain.check_utxo.return_value = True
    with patch("src.scheduler.time.sleep") as mock_sleep:
        mock_sleep.side_effect = [None, KeyboardInterrupt]  # Break after one
        try:
            scheduler.run() # Will loop forever, so patch sleep to break after one
            scheduler.logger.debug.assert_called_with("Checking UTXO status")
        except KeyboardInterrupt:
            pass            #expected result
        scheduler.logger.debug.assert_called_with("Sleeping for 1 seconds")
        scheduler.notifier.notify.assert_called()
