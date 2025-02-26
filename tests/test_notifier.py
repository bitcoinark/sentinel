import pytest
from unittest.mock import Mock, patch
from notifier import Notifier

@pytest.fixture
def logger():
    return Mock()

@pytest.fixture
def notifier(logger):
    return Notifier(
        email_to="test@example.com",
        sms_to="+1234567890",
        smtp_user="user@example.com",
        smtp_pass="pass",
        twilio_sid="sid",
        twilio_token="token",
        twilio_from="+0987654321",
        logger=logger
    )

def test_send_email_success(notifier):
    with patch("smtplib.SMTP") as mock_smtp:
        notifier.send_email("Test message")
        mock_smtp.assert_called_with("smtp.gmail.com", 587)
        notifier.logger.info.assert_called_with("Email sent successfully")

def test_send_email_failure(notifier):
    with patch("smtplib.SMTP", side_effect=Exception("SMTP error")):
        notifier.send_email("Test message")
        notifier.logger.error.assert_called_with("Failed to send email: SMTP error")

def test_send_sms_success(notifier):
    with patch("twilio.rest.Client") as mock_client:
        notifier.send_sms("Test message")
        mock_client.return_value.messages.create.assert_called()
        notifier.logger.info.assert_called_with("SMS sent successfully")

def test_notify_calls_both(notifier):
    with patch.object(notifier, "send_email") as mock_email, patch.object(notifier, "send_sms") as mock_sms:
        notifier.notify("abc123", 0)
        mock_email.assert_called_with("UTXO spent: txid=abc123, vout=0")
        mock_sms.assert_called_with("UTXO spent: txid=abc123, vout=0")
